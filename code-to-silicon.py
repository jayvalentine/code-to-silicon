import os

from testbench import testing

if not os.path.isdir("figures/autogen"):
    os.makedirs("figures/autogen")

testing.runTest("sum_squares")

# Now build the report!
os.system("pdflatex REPORT > texbuild.log")
os.system("biber REPORT > texbuild.log")
os.system("pdflatex REPORT > texbuild.log")
