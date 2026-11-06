// Pilote en ligne de commande pour le coeur SA-PCB (GridBasedPlacer::annealer), sans KicadParser ni SWIG.
// Usage : sa_main entree.txt sortie.txt [-i iter_ext] [-j iter_int] [-t T0] [-s graine] [-m marge] [-w poids_lambda] [-f plancher_sigma]
#include "GridBasedPlacer.hpp"
#include <sstream>

static string o2s(int k) { Node n; return n.orient2str(k); }

int main(int argc, char** argv) {
  if (argc < 3) { cerr << "usage: sa_main in out [opts]" << endl; return 2; }
  int outer = 100, inner = 25, seed = 1; double t0 = 0.5, margin = 0.05, lamsched = 0.95;
  for (int a = 3; a + 1 < argc; a += 2) {
    string k = argv[a]; double v = atof(argv[a + 1]);
    if (k == "-i") outer = (int)v; else if (k == "-j") inner = (int)v; else if (k == "-t") t0 = v;
    else if (k == "-s") seed = (int)v; else if (k == "-m") margin = v; else if (k == "-w") lamsched = v;
  }
  GridBasedPlacer P;
  P.rng.seed(seed); srand(seed);
  ifstream f(argv[1]);
  string line, kw;
  vector<string> names;
  map<int, vector<pPin>> netToCell;
  int curNet = -1;
  while (getline(f, line)) {
    istringstream is(line); is >> kw;
    if (kw == "BOARD") {
      double a, b, c, d; is >> a >> b >> c >> d;
      P.mMinX = a + margin; P.mMinY = b + margin; P.mMaxX = c - margin; P.mMaxY = d - margin;
    } else if (kw == "NODE") {
      string ref; double w, h, cx, cy; int fixed, k; is >> ref >> w >> h >> fixed >> cx >> cy >> k;
      int idx = (int)nodeId.size();
      Node n; n.setParameterNodes(ref, w, h, false, idx, 1, false);
      double W = (k == 2 || k == 6) ? h : w, H = (k == 2 || k == 6) ? w : h;
      n.setParameterPl(cx - W / 2, cy - H / 2, o2s(k), fixed != 0);
      nodeId.push_back(n); name2id[ref] = idx; names.push_back(ref);
    } else if (kw == "NET") {
      int id, np; is >> id >> np; curNet = id; netToCell[id] = vector<pPin>();
    } else if (kw == "PIN") {
      string ref; double dx, dy; is >> ref >> dx >> dy;
      int idx = name2id[ref]; pPin p; p.set_params(ref, dx, dy, idx);
      netToCell[curNet].push_back(p); nodeId[idx].setNetList(curNet);
    }
  }
  P.num_nets = (int)netToCell.size();
  cout << "noeuds " << nodeId.size() << " reseaux " << netToCell.size() << endl;
  P.set_two_sided(true);          // replie la proba "changement de face" dans les deplacements (reste en face F)
  P.set_rtree(true);
  P.set_num_iterations(outer);
  P.set_iterations_moves(inner);
  P.set_initial_temperature(t0);
  P.set_lambda_schedule(lamsched);
  auto t1 = chrono::steady_clock::now();
  P.annealer(netToCell, "");
  if (P.bestSol.size() > 0) nodeId = P.bestSol;
  double oa = P.cell_overlap(), wl = P.wirelength(netToCell);
  double secs = chrono::duration<double>(chrono::steady_clock::now() - t1).count();
  cout << "FINAL overlap " << oa << " wirelength " << wl << " secondes " << secs << endl;
  ofstream o(argv[2]);
  for (auto& n : nodeId)
    o << n.name << " " << n.xBy2 << " " << n.yBy2 << " " << n.orientation << " " << (n.fixed ? 1 : 0) << "\n";
  return 0;
}
