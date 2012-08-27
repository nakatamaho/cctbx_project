from __future__ import division

from libtbx.test_utils import approx_equal
from mmtbx.geometry_restraints import reference_coordinate
import iotbx.pdb
from cctbx.array_family import flex
from cctbx import adp_restraints # import dependency
from mmtbx.monomer_library import server, pdb_interpretation
from cStringIO import StringIO
import random

if(1):
  random.seed(0)
  flex.set_random_seed(0)

def simple_pdb () :
  import iotbx.pdb
  pdb_in = iotbx.pdb.input(source_info=None, lines="""\
CRYST1   36.670   40.710   66.290  90.00  90.00  90.00 P 21 21 21    4
ATOM      1  N   THR A   2      -3.791  -8.769  29.092  1.00 24.15           N
ATOM      2  CA  THR A   2      -3.627  -7.675  28.090  1.00 25.97           C
ATOM      3  C   THR A   2      -2.202  -7.127  28.152  1.00 24.18           C
ATOM      4  O   THR A   2      -1.633  -6.984  29.233  1.00 24.71           O
ATOM      5  CB  THR A   2      -4.627  -6.527  28.357  1.00 26.50           C
ATOM      6  OG1 THR A   2      -5.961  -7.056  28.404  1.00 28.79           O
ATOM      7  CG2 THR A   2      -4.548  -5.486  27.255  1.00 27.05           C
ATOM      8  N   LYS A   3      -1.629  -6.832  26.988  1.00 24.44           N
ATOM      9  CA  LYS A   3      -0.266  -6.307  26.901  1.00 25.16           C
ATOM     10  C   LYS A   3      -0.196  -4.896  27.485  1.00 23.66           C
ATOM     11  O   LYS A   3      -1.094  -4.084  27.265  1.00 23.75           O
ATOM     12  CB  LYS A   3       0.199  -6.262  25.438  1.00 26.61           C
ATOM     13  CG ALYS A   3       0.312  -7.619  24.754  0.50 27.88           C
ATOM     14  CG BLYS A   3       0.201  -7.603  24.718  0.50 27.66           C
ATOM     15  CD ALYS A   3       1.436  -8.454  25.347  0.50 27.58           C
ATOM     16  CD BLYS A   3       1.205  -8.570  25.325  0.50 27.30           C
ATOM     17  CE ALYS A   3       1.585  -9.783  24.621  0.50 28.69           C
ATOM     18  CE BLYS A   3       1.213  -9.893  24.575  0.50 28.17           C
ATOM     19  NZ ALYS A   3       0.362 -10.624  24.732  0.50 28.63           N
ATOM     20  NZ BLYS A   3       2.149 -10.873  25.188  0.50 27.40           N
ATOM     21  N   LYS A   4       0.873  -4.612  28.225  1.00 22.24           N
ATOM     22  CA  LYS A   4       1.068  -3.295  28.826  1.00 21.81           C
ATOM     23  C   LYS A   4       2.337  -2.642  28.295  1.00 19.26           C
ATOM     24  O   LYS A   4       3.417  -3.243  28.310  1.00 18.66           O
ATOM     25  CB  LYS A   4       1.156  -3.398  30.354  1.00 23.29           C
ATOM     26  CG  LYS A   4      -0.170  -3.685  31.031  1.00 27.60           C
ATOM     27  CD  LYS A   4      -0.049  -3.681  32.551  1.00 32.16           C
ATOM     28  CE  LYS A   4       0.797  -4.842  33.052  1.00 33.04           C
ATOM     29  NZ  LYS A   4       0.827  -4.892  34.541  1.00 36.05           N
""")
  return pdb_in

pdb_str_2 = """\
CRYST1   26.960   29.455   29.841  90.00  90.00  90.00 P 21 21 21
ATOM      1  N   TYR A  20      10.702  10.331   8.954  1.00 23.81           N
ATOM      2  CA  TYR A  20      11.170   9.547   7.817  1.00 35.69           C
ATOM      3  C   TYR A  20      10.082   8.601   7.319  1.00 28.94           C
ATOM      4  O   TYR A  20       9.756   7.616   7.982  1.00 25.26           O
ATOM      5  CB  TYR A  20      12.426   8.758   8.192  1.00 33.37           C
ATOM      6  CG  TYR A  20      13.016   7.958   7.052  1.00 31.48           C
ATOM      7  CD1 TYR A  20      13.847   8.558   6.115  1.00 36.91           C
ATOM      8  CD2 TYR A  20      12.747   6.602   6.916  1.00 21.36           C
ATOM      9  CE1 TYR A  20      14.389   7.832   5.071  1.00 36.56           C
ATOM     10  CE2 TYR A  20      13.285   5.868   5.875  1.00 29.56           C
ATOM     11  CZ  TYR A  20      14.105   6.487   4.957  1.00 35.08           C
ATOM     12  OH  TYR A  20      14.644   5.760   3.920  1.00 38.73           O
ATOM     13  N   ARG A  21       9.530   8.915   6.149  1.00 38.95           N
ATOM     14  CA  ARG A  21       8.473   8.118   5.525  1.00 38.77           C
ATOM     15  C   ARG A  21       7.250   7.963   6.428  1.00 27.69           C
ATOM     16  O   ARG A  21       7.134   6.992   7.176  1.00 22.82           O
ATOM     17  CB  ARG A  21       9.004   6.747   5.093  1.00 20.00           C
ATOM     18  CG  ARG A  21       8.015   5.920   4.285  1.00 20.00           C
ATOM     19  CD  ARG A  21       8.608   4.577   3.893  1.00 20.00           C
ATOM     20  NE  ARG A  21       7.671   3.771   3.116  1.00 20.00           N
ATOM     21  CZ  ARG A  21       7.939   2.556   2.649  1.00 20.00           C
ATOM     22  NH1 ARG A  21       9.121   2.001   2.879  1.00 20.00           N
ATOM     23  NH2 ARG A  21       7.025   1.895   1.951  1.00 20.00           N
ATOM     24  N   GLY A  22       6.340   8.929   6.351  1.00 24.85           N
ATOM     25  CA  GLY A  22       5.132   8.903   7.154  1.00 29.53           C
ATOM     26  C   GLY A  22       5.373   9.358   8.580  1.00 33.22           C
ATOM     27  O   GLY A  22       5.196  10.531   8.906  1.00 30.06           O
"""

pdb_str_3 = """\
CRYST1   26.960   29.455   29.841  90.00  90.00  90.00 P 21 21 21
ATOM      1  N   TYR A  20      10.702  10.331   8.954  1.00 23.81           N
ATOM      2  CA  TYR A  20      11.170   9.547   7.817  1.00 35.69           C
ATOM      3  C   TYR A  20      10.082   8.601   7.319  1.00 28.94           C
ATOM      4  O   TYR A  20       9.756   7.616   7.982  1.00 25.26           O
ATOM      5  CB  TYR A  20      12.426   8.758   8.192  1.00 33.37           C
ATOM      6  CG  TYR A  20      13.016   7.958   7.052  1.00 31.48           C
ATOM      7  CD1 TYR A  20      13.847   8.558   6.115  1.00 36.91           C
ATOM      8  CD2 TYR A  20      12.747   6.602   6.916  1.00 21.36           C
ATOM      9  CE1 TYR A  20      14.389   7.832   5.071  1.00 36.56           C
ATOM     10  CE2 TYR A  20      13.285   5.868   5.875  1.00 29.56           C
ATOM     11  CZ  TYR A  20      14.105   6.487   4.957  1.00 35.08           C
ATOM     12  OH  TYR A  20      14.644   5.760   3.920  1.00 38.73           O
ATOM     13  N   ARG A  21       9.530   8.915   6.149  1.00 38.95           N
ATOM     14  CA  ARG A  21       8.473   8.118   5.525  1.00 38.77           C
ATOM     15  C   ARG A  21       7.250   7.963   6.428  1.00 27.69           C
ATOM     16  O   ARG A  21       7.134   6.992   7.176  1.00 22.82           O
ATOM     17  CB  ARG A  21       9.004   6.747   5.093  1.00 20.00           C
ATOM     18  CG  ARG A  21       9.445   5.856   6.245  1.00 20.00           C
ATOM     19  CD  ARG A  21      10.004   4.536   5.740  1.00 20.00           C
ATOM     20  NE  ARG A  21      10.410   3.660   6.835  1.00 20.00           N
ATOM     21  CZ  ARG A  21       9.599   2.802   7.446  1.00 20.00           C
ATOM     22  NH1 ARG A  21       8.331   2.702   7.070  1.00 20.00           N
ATOM     23  NH2 ARG A  21      10.055   2.043   8.433  1.00 20.00           N
ATOM     24  N   GLY A  22       6.340   8.929   6.351  1.00 24.85           N
ATOM     25  CA  GLY A  22       5.132   8.903   7.154  1.00 29.53           C
ATOM     26  C   GLY A  22       5.373   9.358   8.580  1.00 33.22           C
ATOM     27  O   GLY A  22       5.196  10.531   8.906  1.00 30.06           O
"""

def exercise_1():
  pdb_in = simple_pdb()
  mon_lib_srv = server.server()
  ener_lib = server.ener_lib()
  params = pdb_interpretation.master_params.extract()
  processed_pdb_file = pdb_interpretation.process(
    mon_lib_srv=mon_lib_srv,
    ener_lib=ener_lib,
    params=params,
    pdb_inp=pdb_in,
    log=StringIO())
  grm = processed_pdb_file.geometry_restraints_manager()
  pdb_hierarchy = processed_pdb_file.all_chain_proxies.pdb_hierarchy
  sites_cart = pdb_hierarchy.atoms().extract_xyz()
  reference_coordinate_proxies = \
    reference_coordinate.build_proxies(
      sites_cart=sites_cart).reference_coordinate_proxies
  grads = flex.vec3_double(sites_cart.size(), (0.0,0.0,0.0))
  residual = reference_coordinate.target_and_gradients(
               proxies=reference_coordinate_proxies,
               sites_cart=sites_cart,
               gradient_array=grads)
  assert approx_equal(residual, 0.0)

  assert grm.generic_restraints_manager.reference_coordinate_proxies is None

  grm.generic_restraints_manager.add_reference_restraints(
    sites_cart=sites_cart)

  assert grm.generic_restraints_manager.reference_coordinate_proxies \
    is not None
  assert len(grm.generic_restraints_manager.reference_coordinate_proxies) \
    == 29

  #test selection
  ca_selection = pdb_hierarchy.get_c_alpha_selection()
  ca_sites_cart = sites_cart.select(ca_selection)
  grm.generic_restraints_manager.add_reference_restraints(
    sites_cart=ca_sites_cart,
    selection=ca_selection)
  assert len(grm.generic_restraints_manager.reference_coordinate_proxies) \
    == 3
  tst_iselection = flex.size_t()
  for atom in pdb_hierarchy.atoms():
    if atom.name == " CA " or atom.name == " N  ":
      tst_iselection.append(atom.i_seq)
  tst_sites_cart = sites_cart.select(tst_iselection)
  grm.generic_restraints_manager.add_reference_restraints(
    sites_cart=tst_sites_cart,
    selection=tst_iselection)
  assert len(grm.generic_restraints_manager.reference_coordinate_proxies) \
    == 6

  #test remove
  rest = \
    grm.generic_restraints_manager.reference_coordinate_proxies.\
      proxy_remove(selection=flex.bool([True]*29))
  assert rest.size() == 0
  rest = \
    grm.generic_restraints_manager.reference_coordinate_proxies.\
      proxy_remove(selection=flex.bool([False]*29))
  assert rest.size() == 6
  rm_iselection = flex.size_t()
  for atom in pdb_hierarchy.atoms():
    if atom.name == " N  ":
      rm_iselection.append(atom.i_seq)
  selection = flex.bool(len(sites_cart), rm_iselection)
  rest = \
    grm.generic_restraints_manager.reference_coordinate_proxies.\
      proxy_remove(selection=selection)
  assert rest.size() == 3

def exercise_2():
  for use_reference in [True, False]:
    processed_pdb_file = pdb_interpretation.process(
      mon_lib_srv              = server.server(),
      ener_lib                 = server.ener_lib(),
      raw_records              = flex.std_string(pdb_str_2.splitlines()),
      strict_conflict_handling = True,
      force_symmetry           = True,
      log                      = None)
    grm = processed_pdb_file.geometry_restraints_manager()
    xrs2 = processed_pdb_file.xray_structure(show_summary = False)
    awl2 = processed_pdb_file.all_chain_proxies.pdb_hierarchy.atoms_with_labels()
    pdb_inp3 = iotbx.pdb.input(source_info=None, lines=pdb_str_3)
    xrs3 = pdb_inp3.xray_structure_simple()
    ph3 = pdb_inp3.construct_hierarchy()
    ph3.atoms().reset_i_seq()
    awl3 =  ph3.atoms_with_labels()
    sites_cart_reference = flex.vec3_double()
    selection = flex.size_t()
    reference_names = ["CG", "CD", "NE", "CZ", "NH1", "NH2"]
    for a2,a3 in zip(tuple(awl2), tuple(awl3)):
      assert a2.resname == a3.resname
      assert a2.name == a3.name
      assert a2.i_seq == a3.i_seq
      if(a2.resname == "ARG" and a2.name.strip() in reference_names):
        selection.append(a2.i_seq)
        sites_cart_reference.append(a3.xyz)
    assert selection.size() == len(reference_names)
    if(use_reference):
      grm.generic_restraints_manager.add_reference_restraints(
        sites_cart = sites_cart_reference,
        selection = selection,
        sigma = 0.01)
    d1 = flex.mean(flex.sqrt((xrs2.sites_cart().select(selection) -
                              xrs3.sites_cart().select(selection)).dot()))
    print "distance start (use_reference: %s): %6.4f"%(str(use_reference), d1)
    assert d1>4.0
    selection_bool = flex.bool(xrs2.scatterers().size(), selection)
    assert approx_equal(
      flex.max(flex.sqrt((xrs2.sites_cart().select(~selection_bool) -
                          xrs3.sites_cart().select(~selection_bool)).dot())), 0)
    from cctbx import geometry_restraints
    import mmtbx.command_line.geometry_minimization
    import scitbx.lbfgs
    grf = geometry_restraints.flags.flags(default=True)
    sites_cart = xrs2.sites_cart()
    minimized = mmtbx.command_line.geometry_minimization.lbfgs(
      sites_cart                  = sites_cart,
      geometry_restraints_manager = grm,
      sites_cart_selection        = flex.bool(sites_cart.size(), selection),
      geometry_restraints_flags   = grf,
      lbfgs_termination_params = scitbx.lbfgs.termination_parameters(
        max_iterations=5000))
    xrs2.set_sites_cart(sites_cart = sites_cart)
    d2 = flex.mean(flex.sqrt((xrs2.sites_cart().select(selection) -
                              xrs3.sites_cart().select(selection)).dot()))
    print "distance start (use_reference: %s): %6.4f"%(str(use_reference), d2)
    if(use_reference): assert d2<0.005
    else: assert d2>4.0, d2
    assert approx_equal(
      flex.max(flex.sqrt((xrs2.sites_cart().select(~selection_bool) -
                          xrs3.sites_cart().select(~selection_bool)).dot())), 0)

if (__name__ == "__main__") :
  exercise_1()
  exercise_2()
  print "OK"
