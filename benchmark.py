#!/usr/bin/env python3

from benchkit.benchmark import Benchmark

class WordCountBench(Benchmark):

    def __init__(
        self,
        src_dir: PathType,
        nix_attr: str = "word-count",
        command_wrappers: Iterable[CommandWrapper],
        command_attachments: Iterable[CommandAttachment],
        shared_libs: Iterable[SharedLib],
        pre_run_hooks: Iterable[PreRunHook],
        post_run_hooks: Iterable[PostRunHook],
    ) -> None:
        super().__init__(
            command_wrappers=command_wrappers,
            command_attachments=command_attachments,
            shared_libs=shared_libs,
            pre_run_hooks=pre_run_hooks,
            post_run_hooks=post_run_hooks,
        )

        self._src_dir = pathlib.Path(src_dir)
        self._nix_attr = nix_attr

    @property
    def bench_src_path(self) -> pathlib.Path:
        return self._bench_src_path

    @staticmethod
    def get_build_var_names() -> List[str]:
        return []

    @staticmethod
    def get_run_var_names() -> List[str]:
        return [
            "input_file"
        ]

    @staticmethod
    def get_tilt_var_names() -> List[str]:
        return []


    def build_bench(
        self,
        **kwargs,
    ) -> None:

        word_count_path = self.platform.comm.shell(
            command=["nix" "build" f"{self._src_dir}#{self._nix_attr}" "--print-out-paths" "--no-link"],
            output_is_log=True
        ).trim()

        self._word_count_bin = f"{word_count_path}/bin/word_count"

    def single_run(self, input_file, **_kwargs):
        environment = {}
        run_command = ['time' self._word_count_bin input_file]

        wrapped_run_command, wrapped_environment = self._wrap_command(
            run_command=run_command,
            wrapped_run_command=wrapped_run_command,
            current_dir=self._build_dir,
            environment=environment,
            wrapped_environment=wrapped_environment,
            print_output=False
        )
    
