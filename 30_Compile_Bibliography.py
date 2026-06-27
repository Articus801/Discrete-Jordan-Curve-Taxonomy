import os

bib_content = r"""@article{jordan1887,
  author    = {Jordan, Camille},
  title     = {Cours d'Analyse de l'{\'E}cole Polytechnique},
  journal   = {Gauthier-Villars, Paris},
  volume    = {3},
  year      = {1887},
  pages     = {587--594}
}

@book{mandelbrot1982,
  author    = {Mandelbrot, Beno{\^\i}t B.},
  title     = {The Fractal Geometry of Nature},
  publisher = {W. H. Freeman and Company},
  address   = {New York},
  year      = {1982}
}

@article{shannon1948,
  author    = {Shannon, Claude E.},
  title     = {A Mathematical Theory of Communication},
  journal   = {Bell System Technical Journal},
  volume    = {27},
  number    = {3},
  pages     = {379--423},
  year      = {1948}
}

@book{falconer2014,
  author    = {Falconer, Kenneth},
  title     = {Fractal Geometry: Mathematical Foundations and Applications},
  edition   = {3rd},
  publisher = {John Wiley \& Sons},
  address   = {Chichester},
  year      = {2014}
}
"""

if __name__ == "__main__":
    output_filename = "paper.bib"

    with open(output_filename, "w") as bib_file:
        bib_file.write(bib_content)

    print("[30_Compile_Bibliography] Generation Complete.")
    print(f" -> Academic bibliography ledger saved as '{output_filename}'.")
    print(" Your JOSS submission text portfolio is now 100% complete and self-contained.")
