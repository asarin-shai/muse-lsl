#!/usr/bin/python
import sys
import argparse
import json
import os
from .constants import LOG_LEVELS


def _load_config(path):
    if not path:
        return {}
    with open(path, 'r') as f:
        return json.load(f)

class CLI:
    def __init__(self, command):
        # use dispatch pattern to invoke method with same name
        getattr(self, command)()

    def list(self):
        parser = argparse.ArgumentParser(
            description='List available Muse devices.')
        parser.add_argument(
            "-b",
            "--backend",
            dest="backend",
            type=str,
            default="auto",
            help="BLE backend to use. Can be auto, bluemuse, gatt or bgapi.")
        parser.add_argument(
            "-i",
            "--interface",
            dest="interface",
            type=str,
            default=None,
            help=
            "The interface to use, 'hci0' for gatt or a com port for bgapi. WIll auto-detect if not specified"
        )
        parser.add_argument(
            '-l',
            "--log", 
            choices=LOG_LEVELS.keys(),
            dest="log_level",
            default='info',
            help='Set the logging level'
        )
        args = parser.parse_args(sys.argv[2:])
        from . import list_muses
        list_muses(args.backend, args.interface, LOG_LEVELS[args.log_level])

    def stream(self):
        parser = argparse.ArgumentParser(
            description='Start an LSL stream from Muse headset.')
        parser.add_argument(
            "-a",
            "--address",
            dest="address",
            type=str,
            default=None,
            help="Device MAC address.")
        parser.add_argument(
            "-n",
            "--name",
            dest="name",
            type=str,
            default=None,
            help="Name of the device.")
        parser.add_argument(
            "-b",
            "--backend",
            dest="backend",
            type=str,
            default="auto",
            help="BLE backend to use. Can be auto, bluemuse, gatt or bgapi.")
        parser.add_argument(
            "-i",
            "--interface",
            dest="interface",
            type=str,
            default=None,
            help=
            "The interface to use, 'hci0' for gatt or a com port for bgapi.")
        parser.add_argument("-P",
            "--preset",
            type=int,
            default=None,
            help="Select preset which dictates data channels to be streamed")
        parser.add_argument(
            "-p",
            "--ppg",
            default=False,
            action="store_true",
            help="Include PPG data")
        parser.add_argument(
            "-c",
            "--acc",
            default=False,
            action="store_true",
            help="Include accelerometer data")
        parser.add_argument(
            "-g",
            "--gyro",
            default=False,
            action="store_true",
            help="Include gyroscope data")
        parser.add_argument(
            '-d',
            '--disable-eeg',
            dest='disable_eeg',
            action='store_true',
            help="Disable EEG data")
        parser.add_argument(
            '-dl',
            '--disable-light',
            dest='disable_light',
            action='store_true',
            help='Turn off light on the Muse S headband')
        parser.add_argument(
            "-lslt",
            "--lsltime",
            default=False,
            dest='lsl_time',
            action="store_true",
            help="Use pylsl's local_clock() for timestamps instead of Python's time.time()")
        parser.add_argument(
            "-r",
            "--retries",
            default=1,
            dest='retries',
            type=int,
            help="How many times to retry connecting to the device on a failed attempt")
        parser.add_argument(
            '-l',
            "--log", 
            choices=LOG_LEVELS.keys(),
            dest="log_level",
            default='info',
            help='Set the logging level'
        )

        args = parser.parse_args(sys.argv[2:])
        from . import stream

        stream(args.address, args.backend, args.interface, args.name, args.ppg,
               args.acc, args.gyro, args.disable_eeg, args.preset, args.disable_light,
               args.lsl_time, args.retries, LOG_LEVELS[args.log_level])

    def record(self):
        parser = argparse.ArgumentParser(
            description='Record data from an LSL stream.')
        parser.add_argument(
            "-d",
            "--duration",
            dest="duration",
            type=int,
            default=60,
            help="Duration of the recording in seconds.")
        parser.add_argument(
            "-f",
            "--filename",
            dest="filename",
            type=str,
            default=None,
            help="Name of the recording file.")
        parser.add_argument(
            "-dj",
            "--dejitter",
            dest="dejitter",
            type=bool,
            default=False,
            help="Whether to apply dejitter correction to timestamps.")
        parser.add_argument(
            "-t",
            "--type",
            type=str,
            default="EEG",
            help="Data type to record from. Either EEG, PPG, ACC, or GYRO.")

        args = parser.parse_args(sys.argv[2:])
        from . import record
        record(args.duration, args.filename, args.dejitter, args.type)

    def record_direct(self):
        parser = argparse.ArgumentParser(
            description='Record directly from Muse without LSL.')
        parser.add_argument(
            "-a",
            "--address",
            dest="address",
            type=str,
            default=None,
            help="Device MAC address.")
        parser.add_argument(
            "-n",
            "--name",
            dest="name",
            type=str,
            default=None,
            help="Name of the device.")
        parser.add_argument(
            "-b",
            "--backend",
            dest="backend",
            type=str,
            default="auto",
            help="BLE backend to use. Can be auto, bluemuse, gatt or bgapi.")
        parser.add_argument(
            "-i",
            "--interface",
            dest="interface",
            type=str,
            default=None,
            help=
            "The interface to use, 'hci0' for gatt or a com port for bgapi.")
        parser.add_argument(
            "-d",
            "--duration",
            dest="duration",
            type=int,
            default=60,
            help="Duration of the recording in seconds.")
        parser.add_argument(
            "-f",
            "--filename",
            dest="filename",
            type=str,
            default=None,
            help="Name of the recording file.")
        args = parser.parse_args(sys.argv[2:])
        from . import record_direct
        record_direct(args.duration, args.address, args.filename, args.backend,
                      args.interface, args.name)

    def view(self):
        parser = argparse.ArgumentParser(
            description='View EEG data from an LSL stream.')
        parser.add_argument(
            "--config",
            dest="config",
            type=str,
            default=None,
            help="Path to JSON config file for viewer settings.")
        parser.add_argument(
            "-w",
            "--window",
            dest="window",
            type=float,
            default=None,
            help="Window length to display in seconds.")
        parser.add_argument(
            "-s",
            "--scale",
            dest="scale",
            type=float,
            default=None,
            help="Scale in uV.")
        parser.add_argument(
            "-r",
            "--refresh",
            dest="refresh",
            type=float,
            default=None,
            help="Refresh rate in seconds.")
        parser.add_argument(
            "-f",
            "--figure",
            dest="figure",
            type=str,
            default=None,
            help="Window size.")
        parser.add_argument(
            "-v",
            "--version",
            dest="version",
            type=int,
            default=None,
            help=
            "Viewer version (1 or 2) - 1 is the default stable version, 2 is in development (and takes no arguments)."
        )
        parser.add_argument(
            "-b",
            "--backend",
            dest="backend",
            type=str,
            default=None,
            help="Matplotlib backend to use. Default: %(default)s")
        parser.add_argument(
            "--filter",
            dest="filt",
            action="store_true",
            help="Start with bandpass filter enabled")
        parser.add_argument(
            "--no-filter",
            dest="filt",
            action="store_false",
            help="Start with bandpass filter disabled")
        parser.set_defaults(filt=None)
        parser.add_argument(
            "--window-step",
            dest="window_step",
            type=float,
            default=None,
            help="Seconds to increment/decrement window when pressing +/- in viewer v1")
        parser.add_argument(
            "--scale-factor",
            dest="scale_factor",
            type=float,
            default=None,
            help="Scale factor applied when zooming with /* in viewer v1")
        parser.add_argument(
            "--subsample",
            dest="subsample",
            type=int,
            default=None,
            help="Subsampling factor for viewer v1 plotting")
        args = parser.parse_args(sys.argv[2:])

        cfg = _load_config(args.config)
        window = args.window if args.window is not None else cfg.get('window', float(os.getenv('MUSELSL_VIEW_WINDOW', 5.0)))
        scale = args.scale if args.scale is not None else cfg.get('scale', float(os.getenv('MUSELSL_VIEW_SCALE', 100.0)))
        refresh = args.refresh if args.refresh is not None else cfg.get('refresh', float(os.getenv('MUSELSL_VIEW_REFRESH', 0.2)))
        figure = args.figure if args.figure is not None else cfg.get('figure', os.getenv('MUSELSL_VIEW_FIGURE', '15x6'))
        version = args.version if args.version is not None else int(cfg.get('version', int(os.getenv('MUSELSL_VIEW_VERSION', 1))))
        backend = args.backend if args.backend is not None else cfg.get('backend', os.getenv('MUSELSL_VIEW_BACKEND', 'TkAgg'))
        filt = args.filt if args.filt is not None else cfg.get('filt', os.getenv('MUSELSL_VIEW_FILTER', 'true').lower() in ('1', 'true', 'yes', 'on'))
        window_step = args.window_step if args.window_step is not None else float(cfg.get('window_step', os.getenv('MUSELSL_VIEW_WINDOW_STEP', 1.0)))
        scale_factor = args.scale_factor if args.scale_factor is not None else float(cfg.get('scale_factor', os.getenv('MUSELSL_VIEW_SCALE_FACTOR', 1.2)))
        subsample = args.subsample if args.subsample is not None else cfg.get('subsample', os.getenv('MUSELSL_VIEW_SUBSAMPLE'))
        subsample = int(subsample) if subsample is not None else None

        from . import view
        view(window, scale, refresh, figure, version,
             backend, filt=filt, window_step=window_step,
             scale_factor=scale_factor, subsample=subsample)
