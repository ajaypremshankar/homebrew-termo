class MacroCli < Formula
    include Language::Python::Virtualenv
  
    desc "A CLI tool for recording and running macros in the terminal"
    homepage "https://github.com/ajaypremshankar/macro-cli"
    url "https://github.com/ajaypremshankar/homebrew-macro-cli/releases/download/1.0.1/macro_cli-1.0.1.tar.gz"
    sha256 "41a7a775c573e67268046c6d89c8f69381549aecb0257897051e2f858c522ed4"  
    license "MIT"
  
    depends_on "python@3.12"
  
    def install
      virtualenv_install_with_resources
    end
  
    test do
      system "#{bin}/mrec", "--help"
    end
  end
  