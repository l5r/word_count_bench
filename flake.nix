{
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.word-count-src = {
    url = "github:l5r/word_count";
    inputs.nixpkgs.follows = "nixpkgs";
  };
  inputs.benchkit = {
    url = "github:l5r/benchkit";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, flake-utils, word-count-src, benchkit }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in {
        packages = rec {
          benchkit-python = benchkit.legacyPackages.${system}.benchkit-python;
          benchkit-python-dev = pkgs.python3.withPackages (ps: [
            benchkit.legacyPackages.${system}.benchkit-python
            ps.python-lsp-server
            ps.python-lsp-server.optional-dependencies.rope
            ps.python-lsp-server.optional-dependencies.pyflakes
          ]);

          word-count = word-count-src.legacyPackages.${system}.default;
        };
      });
}
