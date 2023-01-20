{
  
  inputs = {
    flake-utils.url = "github:numtide/flake-utils/master";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      rec {
        hiro = ({ buildPythonPackage, croniter, cytoolz, pytest, hypothesis }: buildPythonPackage {
          name = "hiro";
          version = "0.0.1";
          src = ./.;
          buildInputs = [ croniter cytoolz ];
          checkInputs = [ pytest hypothesis ];
        });
        packages.default = pkgs.python3Packages.callPackage hiro {};
        devShell = pkgs.mkShell {
          buildInputs = [
            (pkgs.python310.withPackages (ps: with ps; [
              croniter
              cytoolz
              pytest
              hypothesis
            ]))
          ];
        };
      }
    );
}
