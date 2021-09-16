# Tool

See [gillespy-kappa-comparison.md](kappa/gillespy-kappa-comparison.md) for a comparison of Kappa and Gillespy simulation of the toy example.

**v0.2.1** - completely rewrote the Gillespy2 parser, which is now maintainable and uses the simpler **.mln** language compared to **.ste**.

**v0.2.0** - added Kappa parsing functionality to the parser. MLN configuration files can now be exported into Kappa.

**v0.1.0** - rudimentary implementation of a GUI interface and a Gillespie-based simulation. The application takes in two configuration files: model specification using the language prototype (**.mln**) and network specification (**.txt**).