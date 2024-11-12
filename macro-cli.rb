class MacroCli < Formula
    include Language::Python::Virtualenv
  
    desc "A CLI tool for recording and running macros in the terminal"
    homepage "https://github.com/ajaypremshankar/macro-cli"
    url "https://github.com/ajaypremshankar/homebrew-macro-cli/releases/download/1.0.1/macro_cli-1.0.1.tar.gz"
    sha256 "8db3183bd61e2df9bb980b8b1c6e8e0ba87dbe3240eff5044b63dc56135b4c16"  
    license "MIT"
  
    depends_on "python@3.12"

    # Resource for click, only for Python 3.12 and above
    resource "click" do
    url "https://files.pythonhosted.org/packages/96/d3/f04c7bfcf5c1862a2a5b845c6b2b360488cf47af55dfa79c98f6a6bf98b5/click-8.1.7.tar.gz"
    sha256 "ca9853ad459e787e2192211578cc907e7594e294c7ccc834310722b41b9ca6de"
    end
  
    def install
      virtualenv_install_with_resources
    end
  
    test do
      system "#{bin}/mrec", "--help"
    end
  end
  