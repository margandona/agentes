import argparse
from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('upscale_core',ROOT/'scripts/upscale.py')
core=importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


class UnitTests(unittest.TestCase):
    def test_gpu_selection(self):
        devices=[{'index':0,'name':'AMD integrada','device_type':1},
                 {'index':1,'name':'NVIDIA RTX','device_type':2}]
        self.assertEqual(core.choose_gpu(devices),1)
        self.assertEqual(core.choose_gpu(devices,0),0)
        with self.assertRaises(core.UpscaleError):
            core.choose_gpu(devices,7)
        with self.assertRaises(core.UpscaleError):
            core.choose_gpu([])

    def test_bitrate_reference(self):
        self.assertEqual(core.bitrate('30000/1001'),'8M')
        self.assertEqual(core.bitrate('60000/1001'),'12M')


class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            cls.ffmpeg=core.find_tool('ffmpeg')
            cls.ffprobe=core.find_tool('ffprobe')
        except core.UpscaleError as exc:
            raise unittest.SkipTest(str(exc))

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.dir=Path(self.temp.name)

    def fixture(self,name='vídeo ñ con espacios.mp4',fps='30000/1001',audio=True,hdr=False,offset=False):
        path=self.dir/name
        cmd=[self.ffmpeg,'-v','error','-f','lavfi','-i',f'testsrc2=size=96x160:rate={fps}']
        if audio:
            cmd+=['-f','lavfi','-i','sine=frequency=440:sample_rate=48000']
        cmd+=['-vf',f'setparams=color_primaries=bt709:color_trc={"smpte2084" if hdr else "bt709"}:colorspace=bt709:range=limited',
              '-t','0.32','-c:v','libx264','-pix_fmt','yuv420p',
              '-colorspace','bt709','-color_primaries','bt709','-color_trc','smpte2084' if hdr else 'bt709','-color_range','tv']
        if audio:
            cmd+=['-c:a','aac']
        if offset:
            cmd+=['-output_ts_offset','0.08']
        core.execute([*cmd,path])
        return path

    def options(self,source,output,**kwargs):
        args=argparse.Namespace(input=source,output=output,mode='fast',preset='youtube-shorts-1080p',
                                sharpness=0,ai_strength=0.35,seconds=None,ffmpeg=self.ffmpeg,
                                ffprobe=self.ffprobe,engine=None,gpu=None,tile=128,work_dir=None,keep_work=False)
        vars(args).update(kwargs)
        return args

    def test_fractional_fps_color_audio_and_backup(self):
        source=self.fixture()
        before=core.sha256(source)
        result=core.run_job(self.options(source,self.dir/'final.mp4'))
        self.assertTrue(all(result['checks'].values()))
        self.assertEqual(Fraction(result['output_info']['fps']),Fraction(30000,1001))
        self.assertEqual(core.sha256(Path(result['backup'])),before)
        self.assertEqual(core.sha256(source),before)
        hashes=[core.execute([self.ffmpeg,'-v','error','-i',path,'-map','0:a:0','-f','streamhash','-hash','sha256','-'])
                for path in (source,Path(result['output']))]
        self.assertEqual(hashes[0],hashes[1])

    def test_nonzero_start_and_silent_video(self):
        source=self.fixture(fps='25',audio=False,offset=True)
        result=core.run_job(self.options(source,self.dir/'silent.mp4'))
        self.assertEqual(result['output_info']['audio'],[])
        self.assertTrue(result['checks']['video_start'])
        self.assertAlmostEqual(result['input_info']['start'],result['output_info']['start'],places=3)

    def test_overwrite_and_original_are_protected(self):
        source=self.fixture(audio=False)
        digest=core.sha256(source)
        with self.assertRaises(core.UpscaleError):
            core.run_job(self.options(source,source))
        out=self.dir/'exists.mp4'
        out.write_bytes(b'existing')
        with self.assertRaises(core.UpscaleError):
            core.run_job(self.options(source,out))
        self.assertEqual(out.read_bytes(),b'existing')
        self.assertEqual(core.sha256(source),digest)

    def test_invalid_hdr_and_corrupt(self):
        source=self.fixture(hdr=True)
        with self.assertRaisesRegex(core.UpscaleError,'HDR'):
            core.run_job(self.options(source,self.dir/'hdr-out.mp4'))
        bad=self.dir/'broken.mp4'
        bad.write_bytes(b'invalid container')
        with self.assertRaises(core.UpscaleError):
            core.probe(bad,self.ffprobe)

    def test_vfr_is_not_silently_flattened_by_quality(self):
        source=self.fixture(fps='25',audio=False)
        vfr=self.dir/'variable.mp4'
        core.execute([self.ffmpeg,'-v','error','-i',source,'-vf','setpts=(N+floor(N/3))*0.04/TB',
                      '-fps_mode','vfr','-c:v','libx264',vfr])
        self.assertFalse(core.probe(vfr,self.ffprobe)['cfr'])
        with self.assertRaisesRegex(core.UpscaleError,'VFR'):
            core.run_job(self.options(vfr,self.dir/'vfr-ai.mp4',mode='quality'))

    def test_batch_continues_after_corrupt_file(self):
        inputs=self.dir/'inputs'
        inputs.mkdir()
        (inputs/'bad.mp4').write_bytes(b'broken')
        self.fixture(name='inputs/good.mp4',audio=False,fps='25')
        proc=subprocess.run([sys.executable,str(ROOT/'scripts/upscale.py'),'batch',str(inputs),
                             '--output-dir',str(self.dir/'results'),'--mode','fast',
                             '--ffmpeg',self.ffmpeg,'--ffprobe',self.ffprobe],capture_output=True,encoding='utf-8')
        self.assertEqual(proc.returncode,1,proc.stderr)
        report=json.loads(proc.stdout)
        self.assertEqual(report['total'],2)
        self.assertEqual(sum(r['ok'] for r in report['results']),1)

    def test_preview_outputs_full_and_detail(self):
        source=self.fixture(audio=False,fps='25')
        fast=self.dir/'fast.mp4'
        core.run_job(self.options(source,fast))
        result=core.preview(source,fast,fast,self.dir/'preview',self.ffmpeg,self.ffprobe)
        self.assertTrue(result['images'])
        self.assertTrue(all(Path(p).is_file() for p in result['images']))
        self.assertIsNone(result['selection'])

    def test_quality_real_engine_color_timestamps(self):
        try:
            engine=core.find_tool('realesrgan-ncnn-vulkan')
        except core.UpscaleError as exc:
            self.skipTest(str(exc))
        if not core.vulkan_devices()['available']:
            self.skipTest('No hay GPU Vulkan')
        source=self.fixture(fps='25',offset=True)
        result=core.run_job(self.options(source,self.dir/'ai.mp4',mode='quality',engine=engine))
        self.assertTrue(all(result['checks'].values()))
        self.assertEqual(result['output_info']['video']['color_transfer'],'bt709')
        self.assertEqual(result['output_info']['video']['color_primaries'],'bt709')


if __name__=='__main__':
    unittest.main()
