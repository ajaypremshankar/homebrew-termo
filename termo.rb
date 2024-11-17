class Termo < Formula
    include Language::Python::Virtualenv
  
    desc "A CLI tool for recording and running macros in the terminal"
    homepage "https://github.com/ajaypremshankar/homebrew-termo/"
    url "https://github.com/ajaypremshankar/homebrew-termo/releases/download/1.1.1/termo.tar.gz"
    sha256 "c999986993aa0e5685d6cbcac5cfd86c30a6dc105e9d7b6ead686ac6fb277614"  
    license "MIT"
  
    depends_on "python@3.12"

    resource "click" do
    url "https://files.pythonhosted.org/packages/96/d3/f04c7bfcf5c1862a2a5b845c6b2b360488cf47af55dfa79c98f6a6bf98b5/click-8.1.7.tar.gz"
    sha256 "ca9853ad459e787e2192211578cc907e7594e294c7ccc834310722b41b9ca6de"
    end

    resource "paramiko" do
      url "https://files.pythonhosted.org/packages/1b/0f/c00296e36ff7485935b83d466c4f2cf5934b84b0ad14e81796e1d9d3609b/paramiko-3.5.0.tar.gz"
      sha256 "ad11e540da4f55cedda52931f1a3f812a8238a7af7f62a60de538cd80bb28124"
      end
  
    def install
      virtualenv_install_with_resources
    end
  
    test do
      system "#{bin}/tm", "--help"
    end
  end
  