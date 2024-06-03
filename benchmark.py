#!/usr/bin/env python3

import pathlib
import os
from typing import Any, Dict, Iterable, List, Optional

from benchkit.benchmark import Benchmark, CommandAttachment, PostRunHook, PreRunHook
from benchkit.campaign import CampaignCartesianProduct, Constants, CampaignSuite
from benchkit.commandwrappers import CommandWrapper
# from benchkit.dependencies.packages import PackageDependency
from benchkit.platforms import Platform
from benchkit.sharedlibs import SharedLib
from benchkit.utils.types import CpuOrder, PathType



class WordCountBench(Benchmark):

    def __init__(
        self,
        src_dir: PathType,
        command_wrappers: Iterable[CommandWrapper],
        command_attachments: Iterable[CommandAttachment],
        shared_libs: Iterable[SharedLib],
        pre_run_hooks: Iterable[PreRunHook],
        post_run_hooks: Iterable[PostRunHook],
        platform: Platform | None = None,
        build_dir: PathType | None = None,
    ) -> None:
        super().__init__(
            command_wrappers=command_wrappers,
            command_attachments=command_attachments,
            shared_libs=shared_libs,
            pre_run_hooks=pre_run_hooks,
            post_run_hooks=post_run_hooks,
        )

        self._src_dir = pathlib.Path(src_dir)
        self._bench_src_path = self._src_dir
        self._build_dir = build_dir

    @property
    def bench_src_path(self) -> pathlib.Path:
        return self._bench_src_path

    @staticmethod
    def get_build_var_names() -> List[str]:
        return [
            "nix_attr"
        ]

    @staticmethod
    def get_run_var_names() -> List[str]:
        return [
            "input_file"
        ]

    @staticmethod
    def get_tilt_var_names() -> List[str]:
        return []

    def clean_bench(self) -> None:
        pass
    def prebuild_bench(self, **kwargs):
        pass

    def build_bench(
        self,
        nix_attr="word-count",
        **kwargs,
    ) -> None:

        word_count_path = self.platform.comm.shell(
            command=["nix", "build", f"{self._src_dir}#{nix_attr}", "--print-out-paths", "--no-link"],
            output_is_log=True
        ).strip()

        self._word_count_bin = f"{word_count_path}/bin/word_count"

    def single_run(self, input_file, **kwargs):
        output_file = '/tmp/word_count.txt'
        environment = {}
        run_command = [self._word_count_bin, str(input_file), output_file]

        wrapped_run_command, wrapped_environment = self._wrap_command(
            run_command=run_command,
            environment=environment,
            **kwargs,
        )

        output = self.run_bench_command(
            run_command=run_command,
            environment=environment,
            wrapped_run_command=wrapped_run_command,
            wrapped_environment=wrapped_environment,
            current_dir=self._build_dir,
            print_output=False
        )

        return output

    def parse_output_to_results(self, command_output: str, **kwargs):
        lines = command_output.splitlines()

        print(lines)

        import re

        METRIC_REGEX = re.compile("(.+): (\d+)ms")
        matches = [METRIC_REGEX.match(line).group(1, 2) for line in lines]
        return dict([(name, int(value)) for (name, value) in matches])

def word_count_campaign(
    name: str = "word_count_campaign",
    benchmark: Optional[WordCountBench] = None,
    src_dir: Optional[PathType] = None,
    build_dir: Optional[str] = None,
    results_dir: Optional[PathType] = None,
    command_wrappers: Iterable[CommandWrapper] = (),
    command_attachments: Iterable[CommandAttachment] = (),
    shared_libs: Iterable[SharedLib] = (),
    pre_run_hooks: Iterable[PreRunHook] = (),
    post_run_hooks: Iterable[PostRunHook] = (),
    platform: Platform | None = None,
    nb_runs: int = 3,
    benchmark_duration_seconds: int = 5,

    input_file: Iterable[PathType] = (),
    nix_attr: Iterable[str] = ("word-count", "word-count-cpp"),
    
    debug: bool = False,
    gdb: bool = False,
    enable_data_dir: bool = False,
    continuing: bool = False,
    constants: Constants = None,
    pretty: Optional[Dict[str, str]] = None,
):
    if src_dir != None:
        src_dir = pathlib.Path(src_dir)
    else:
        src_dir = pathlib.Path(__file__).parent.resolve()

    variables = {
        "input_file": input_file or (str(src_dir / "random.txt"),),
        "nix_attr": nix_attr,
    }

    if benchmark is None:
        benchmark = WordCountBench(
            src_dir=src_dir,
            command_wrappers=command_wrappers,
            command_attachments=command_attachments,
            shared_libs=shared_libs,
            pre_run_hooks=pre_run_hooks,
            post_run_hooks=post_run_hooks,
            platform=platform,
            build_dir=build_dir,
        )

    return CampaignCartesianProduct(
        name=name,
        benchmark=benchmark,
        nb_runs=nb_runs,
        variables=variables,
        constants=constants,
        debug=debug,
        gdb=gdb,
        enable_data_dir=enable_data_dir,
        continuing=continuing,
        benchmark_duration_seconds=benchmark_duration_seconds,
        results_dir=results_dir,
        pretty=pretty,
    )

def main() -> None:
    src_dir = os.environ.get("SRC_DIR", None)
    campaign = word_count_campaign(src_dir=src_dir)
    campaigns = [campaign]
    suite = CampaignSuite(campaigns=campaigns)
    suite.print_durations()
    suite.run_suite()

if __name__ == '__main__':
    main()
    
