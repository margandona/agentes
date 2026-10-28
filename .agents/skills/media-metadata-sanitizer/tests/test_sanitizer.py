import importlib.util
import json
from pathlib import Path
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('sanitizer_core', ROOT / 'scripts/core.py')
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


class UnitTests(unittest.TestCase):
    def test_classification(self):
        for key, expected in [('EXIF:Software', 'software'), ('GPS:GPSLatitude', 'location'),
                              ('XMP-dc:Creator', 'personal'), ('EXIF:DateTimeOriginal', 'dates'),
                              ('XMP-dc:Rights', 'provenance'), ('JUMBF:Manifest', 'provenance'),
                              ('File:FileModifyDate', 'structural'), ('EXIF:Orientation', 'other')]:
            self.assertEqual(core.category(key), expected)

    def test_missing_dependency(self):
        with patch.object(core.shutil, 'which', return_value=None):
            with self.assertRaisesRegex(core.MediaError, 'Falta ffprobe'):
                core.run(['ffprobe', 'x'])

    def test_provenance_chunk_boundary(self):
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp) / 'fixture'
            p.write_bytes(b'x' * (1024 * 1024 - 2) + b'c2pa')
            self.assertEqual(core.provenance_markers(p), ['c2pa'])

    def test_bmff_provenance_is_not_compressed_media_text(self):
        def box(kind, payload):
            return struct.pack('>I4s',len(payload)+8,kind)+payload
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'fixture.mp4'
            ftyp=box(b'ftyp',b'isom'+b'\x00'*4+b'isom')
            p.write_bytes(ftyp+box(b'mdat',b'compressed-C2PA-random-bytes')+box(b'moov',b''))
            self.assertEqual(core.provenance_markers(p),[])
            p.write_bytes(ftyp+box(b'mdat',b'payload')+box(b'moov',b'c2pa'))
            self.assertIn('c2pa',core.provenance_markers(p))
            uuid=bytes.fromhex('d8fec3d61b0e483c92975828877ec481')
            p.write_bytes(ftyp+box(b'uuid',uuid+b'\x00'*16)+box(b'mdat',b'payload'))
            self.assertIn('c2pa_uuid',core.provenance_markers(p))
            p.write_bytes(ftyp+box(b'mdat',b'C2PA')+b'malformed')
            self.assertIn('c2pa',core.provenance_markers(p))

    def test_existing_output_and_protected(self):
        with tempfile.TemporaryDirectory() as temp:
            p, out = Path(temp) / 'in.mp4', Path(temp) / 'out.mp4'
            p.write_bytes(b'original')
            report = {'path': str(p), 'format': 'MP4', 'protected_indicators': ['c2pa'], 'metadata': {}}
            with patch.object(core, 'inspect_media', return_value=report):
                with self.assertRaisesRegex(core.MediaError, 'procedencia protegida'):
                    core.sanitize(p, out, ['software'])
                self.assertFalse(out.exists())
                out.write_bytes(b'existing')
                with self.assertRaisesRegex(core.MediaError, 'ya existe'):
                    core.sanitize(p, out, ['software'])
                self.assertEqual(out.read_bytes(), b'existing')
                self.assertEqual(p.read_bytes(), b'original')

    def test_batch_isolation(self):
        with tempfile.TemporaryDirectory() as temp:
            src, dst = Path(temp) / 'src', Path(temp) / 'dst'
            src.mkdir()
            (src / 'bad').write_bytes(b'bad')
            (src / 'good').write_bytes(b'good')
            with patch.object(core, 'sanitize', side_effect=[core.MediaError('dañado'), {'ok': True}]):
                report = core.batch(src, dst, ['software'])
            self.assertEqual(report['total'], 2)
            self.assertEqual(report['succeeded'], 1)
            self.assertFalse(report['ok'])
            with self.assertRaises(core.MediaError):
                core.batch(src, src / 'nested', ['software'])

    def test_cli_help(self):
        for name in ('inspect', 'sanitize', 'verify', 'batch'):
            proc = subprocess.run([sys.executable, str(ROOT / 'scripts' / f'{name}.py'), '--help'], capture_output=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)


@unittest.skipUnless(all(shutil.which(x) for x in ('ffmpeg', 'ffprobe', 'exiftool')), 'Faltan FFmpeg/FFprobe/ExifTool en PATH')
class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir = Path(self.temp.name)

    def video(self, suffix):
        p = self.dir / ('vídeo de prueba ' + suffix[1:] + suffix)
        core.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=blue:s=64x48:r=10',
                  '-f', 'lavfi', '-i', 'sine=frequency=440', '-t', '0.5', '-c:v',
                  'libvpx-vp9' if suffix == '.webm' else 'mpeg4', '-c:a',
                  'libopus' if suffix == '.webm' else 'aac', '-metadata', 'artist=Persona ficticia',
                  '-metadata', 'title=Conservar título', p])
        return p

    def test_video_formats(self):
        for suffix in ('.mp4', '.mov', '.mkv', '.webm'):
            with self.subTest(suffix=suffix):
                p = self.video(suffix)
                original = core.sha256(p)
                out = self.dir / ('limpio' + suffix)
                report = core.sanitize(p, out, ['personal'])
                self.assertTrue(report['ok'])
                self.assertEqual(core.sha256(p), original)
                self.assertEqual(len(core.inspect_media(out)['probe']['streams']), 2)
                self.assertTrue(any(v['value'] == 'Conservar título' for v in report['remaining'].values()))
                with self.assertRaises(core.MediaError):
                    core.sanitize(p, out, ['personal'])
                self.assertEqual(report['residual_selected'], {})
                json.dumps(report)

    def test_image_formats(self):
        for suffix in ('.jpg', '.png', '.webp'):
            with self.subTest(suffix=suffix):
                p = self.dir / ('imagen ñ' + suffix)
                core.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i', 'color=c=red:s=64x48', '-frames:v', '1', p])
                core.run(['exiftool', '-overwrite_original', '-XMP:CreatorTool=Herramienta ficticia', p])
                before = core.sha256(p)
                result = core.sanitize(p, self.dir / ('limpia' + suffix), ['software'])
                self.assertTrue(result['ok'])
                self.assertEqual(before, core.sha256(p))

    def test_corrupt_and_misnamed(self):
        bad = self.dir / 'roto.mp4'
        bad.write_bytes(b'not media')
        with self.assertRaises(core.MediaError):
            core.inspect_media(bad)
        p = self.video('.mp4')
        renamed = p.with_suffix('.png')
        p.rename(renamed)
        self.assertEqual(core.inspect_media(renamed)['format'], 'MP4')
        out = self.dir / 'dry.mp4'
        self.assertTrue(core.sanitize(renamed, out, ['personal'], True)['dry_run'])
        self.assertFalse(out.exists())

    def test_verify_detects_content_change(self):
        p = self.video('.mp4')
        altered = self.dir / 'altered.mp4'
        core.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', 'negate', '-c:v', 'mpeg4', '-c:a', 'copy', altered])
        self.assertFalse(core.compare(core.inspect_media(p), core.inspect_media(altered))['ok'])

    def test_preserves_nonzero_start_audio(self):
        p = self.video('.mp4')
        shifted = self.dir / 'shifted.mp4'
        core.run(['ffmpeg', '-v', 'error', '-i', p, '-map', '0', '-c', 'copy',
                  '-output_ts_offset', '0.06', shifted])
        result = core.sanitize(shifted, self.dir / 'clean-shifted.mp4', ['personal', 'software', 'dates', 'location'])
        self.assertTrue(result['checks']['decoded_content'])


if __name__ == '__main__':
    unittest.main()
