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
        hiro = ({ buildPythonPackage, croniter, cytoolz, pytest }: buildPythonPackage {
          name = "hiro";
          version = "0.0.1";
          src = ./.;
          propagatedBuildInputs = [ croniter cytoolz ];
          checkInputs = [ pytest ];
          checkPhase = ''python -m pytest'';
        });

        packages.hiro-package = pkgs.python3Packages.callPackage hiro {};
        packages.hiro = pkgs.python3Packages.toPythonApplication packages.hiro-package;
        packages.default = packages.hiro-package;

        apps.hiro = flake-utils.lib.mkApp { drv = packages.hiro; };
        apps.default = apps.hiro;

        devShell = pkgs.mkShell {
          buildInputs = [
            (pkgs.python310.withPackages (ps: with ps; [
              croniter
              cytoolz
              pytest
            ]))
          ];
        };
      }
    );
}
