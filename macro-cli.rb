class MacroCli < Formula
    include Language::Python::Virtualenv
  
    desc "A CLI tool for recording and running macros in the terminal"
    homepage "https://github.com/ajaypremshankar/macro-cli"  # replace with your repo URL
    url "https://github.com/ajaypremshankar/macro-cli/releases/download/1.0.0/macro_cli-1.0.tar.gz"  # replace with the URL of your .tar.gz
    sha256 "a56e66b267497c1abfc58b27fc399f7df20de6abe318145b9ed2d04f04b37a54"  # replace with the SHA256 hash
    license "MIT"
  
    depends_on "python@3.12"  # Specify Python version if needed
  
    def install
      virtualenv_install_with_resources
    end
  
    test do
      system "#{bin}/macro", "--help"
    end
  end
  