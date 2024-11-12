class MacroCli < Formula
    include Language::Python::Virtualenv
  
    desc "A CLI tool for recording and running macros in the terminal"
    homepage "https://github.com/ajaypremshankar/macro-cli"  # replace with your repo URL
    url "https://github.com/ajaypremshankar/homebrew-macro-cli/releases/download/1.0.1/macro_cli-1.0.1.tar.gz"  # replace with the URL of your .tar.gz
    sha256 "fea7bbc9becf5ed1ff45dfb05e83afb6636e4a6aa509da7e9948069518cabbfc"  # replace with the SHA256 hash
    license "MIT"
  
    depends_on "python@3.12"  # Specify Python version if needed
  
    def install
      virtualenv_install_with_resources
    end
  
    test do
      system "#{bin}/macro", "--help"
    end
  end
  