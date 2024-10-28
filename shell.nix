{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python311
    pkgs.python311Packages.python-telegram-bot
    pkgs.python311Packages.openai
    pkgs.python311Packages.pymupdf
  ];
}
