def print_header():
  import sys
  print """/* Copyright (c) 2001 The Regents of the University of California through
   E.O. Lawrence Berkeley National Laboratory, subject to approval by the
   U.S. Department of Energy. See files COPYRIGHT.txt and
   cctbx/LICENSE.txt for further details.

   Revision history:
     2002 Apr: split into blocks; energies not explicitly tabulated (rwgk)
     Apr 2001: SourceForge release (R.W. Grosse-Kunstleve)
               Based on C code contributed by Vincent Favre-Nicolin.

   *****************************************************
   THIS IS AN AUTOMATICALLY GENERATED FILE. DO NOT EDIT.
   *****************************************************

   Generated by:
     %s
 */

#include <cctbx/constants.h>
#include <cctbx/eltbx/basic.h>
#include <cctbx/eltbx/sasaki.h>

// BEGIN_COMPILED_IN_REFERENCE_DATA
namespace cctbx { namespace eltbx { namespace detail { namespace sasaki {
""" % (sys.argv[0],)

def print_ftp_info():
  print """/*
  Sasaki Tables

  Scattering factors based on the Cromer and Liberman method.
  Original data can be downloaded from:
  ftp://pfweis.kek.jp/pub/Sasaki-table/
  Any reports or publications of these data will acknowledge
  its use by the citation:
    Anomalous scattering factors
        S.Sasaki (1989) Numerical Tables of Anomalous Scattering Factors
        Calculated by the Cromer and Liberman Method,
        KEK Report, 88-14, 1-136
  Questions about these data should be addressed to Dr.Satoshi Sasaki,
  Tokyo Institute of Technology.  Email: sasaki@nc.titech.ac.jp
 */
"""

class sasaki_table:

  def __init__(self, atomic_symbol, atomic_number,
               edge_label=0, edge_wave_length=0):
    assert edge_label in (0, "K", "L1", "L2", "L3")
    self.atomic_symbol = atomic_symbol.lower().capitalize()
    self.atomic_number = atomic_number
    self.edge_label = edge_label
    self.edge_wave_length = edge_wave_length
    self.fp = []
    self.fdp = []

  def check_first_last(self, i_block, first, last):
    assert abs(
      self.first + (i_block * self.incr1000) / 1000. - first) < 1.e-8
    assert abs(first + 9 * self.incr1000 / 10000. - last) < 1.e-8

  def validate(self):
    assert len(self.fp) == len(self.fdp)
    assert len(self.fp) == 280

def collect_tables(file_object, edge):
  import re
  tables = []
  table = 0
  for line in file_object.xreadlines():
    if (not edge):
      m = re.match(
        r"ATOMIC SYMBOL\s+=\s+(\S+)\s+ATOMIC NUMBER\s+=\s+(\d+)", line)
    else:
      m = re.match(
        r"ATOMIC SYMBOL\s+=\s+(\S+)\s+ATOMIC NUMBER\s+=\s+(\d+)"
        + r"\s+(\S+)\s+ABSORPTION EDGE\s+\(\s*(\S+)\s+A", line)
    if (m):
      if (table != 0):
        table.validate()
        tables.append(table)
      if (not edge):
        table = sasaki_table(m.group(1), m.group(2))
      else:
        table = sasaki_table(m.group(1), m.group(2), m.group(3), m.group(4))
      i_block = 0
      continue
    flds = line.split()
    if (flds[1] == "TO"):
      assert flds[3] == "F'"
      first, last = [float(flds[i]) for i in (0, 2)]
      flds = flds[4:]
      if (i_block == 0):
        table.first = 0.1
        table.incr1000 = 100
      table.check_first_last(i_block, first, last)
      i_block += 1
      table.fp += flds
    elif (flds[0].find(",") >= 0):
      assert flds[1] == "F'"
      first, last = [float(x) for x in flds[0].split(",")]
      flds = flds[2:]
      if (i_block == 0):
        table.first = first
        table.incr1000 = 1
      table.check_first_last(i_block, first, last)
      i_block += 1
      table.fp += flds
    else:
      assert flds[0] == 'F"'
      flds = flds[1:]
      table.fdp += flds
    assert len(flds) == 10
  if (table != 0):
    table.validate()
    tables.append(table)
  return tables

class table_references:

  def __init__(self, wide):
    self.wide = wide
    self.k = 0
    self.l1 = 0
    self.l2 = 0
    self.l3 = 0

def combine_tables(tables_wide, tables_k, tables_l):
  ctab_dict = {}
  for w in tables_wide:
    ctab_dict[w.atomic_symbol] = table_references(w)
  for k in tables_k:
    ctab_dict[k.atomic_symbol].k = k
  for l in tables_l:
    if (l.edge_label == "L1"):
      ctab_dict[l.atomic_symbol].l1 = l
    elif (l.edge_label == "L2"):
      ctab_dict[l.atomic_symbol].l2 = l
    else:
      assert l.edge_label == "L3"
      ctab_dict[l.atomic_symbol].l3 = l
  ctab_list = []
  for w in tables_wide:
    ctab_list.append(ctab_dict[w.atomic_symbol])
  return ctab_list

def print_table_block(tables_combined, i_begin, i_end):
  for i_table in xrange(i_begin, i_end):
    ctab = tables_combined[i_table]
    for edge in (ctab.wide, ctab.k, ctab.l1, ctab.l2, ctab.l3):
      if (not edge): continue
      lbl = edge.atomic_symbol
      ann = "Z = " + str(ctab.wide.atomic_number)
      if (edge.edge_label):
        lbl += "_" + edge.edge_label
        ann += "; edge at " + edge.edge_wave_length + " A"
      print "raw " + lbl + "[] = { // " + ann
      for i in xrange(len(edge.fp)):
        print "{%s,%s}," % (edge.fp[i], edge.fdp[i])
      print "};"
  print "}}}} // namespace cctbx::eltbx::detail::sasaki"
  print "// END_COMPILED_IN_REFERENCE_DATA"

def print_sasaki_cpp(tables_combined):
  for ctab in tables_combined:
    print "extern raw " + ctab.wide.atomic_symbol + "[];"
    for edge in (ctab.k, ctab.l1, ctab.l2, ctab.l3):
      if (edge):
        assert edge.atomic_symbol == ctab.wide.atomic_symbol
        print "extern raw " + edge.atomic_symbol \
          + "_" + edge.edge_label + "[];"
  print
  print "static const info tables[] = {"
  i = 0
  for ctab in tables_combined:
    i += 1
    out = '{"' + ctab.wide.atomic_symbol + '", ' + str(ctab.wide.atomic_number)
    out += ", " + ctab.wide.atomic_symbol
    for edge in (ctab.k, ctab.l1, ctab.l2, ctab.l3):
      if (edge):
        out += ", %.4f" % (edge.first,)
        out += ", " + edge.atomic_symbol + "_" + edge.edge_label
      else:
        out += ", 0., 0"
    out += "},"
    print out
  print "{0, 0, 0, 0., 0, 0., 0, 0., 0, 0., 0}"
  print "};"
  print """
  }} // namespace detail::sasaki
  // END_COMPILED_IN_REFERENCE_DATA

  Sasaki::Sasaki(const std::string& Label, bool Exact)
  {
    std::string WorkLabel = StripLabel(Label, Exact);
    m_info = detail::FindEntry(detail::sasaki::tables, WorkLabel, Exact);
  }

  namespace detail { namespace sasaki {

    long find_table_interval(double given, double first, double incr,
                             double tolerance = 1.e-8)
    {
      double span = (n_raw - 1) * incr;
      double f = (given - first) / span;
      if (f < -tolerance || f > (1.+tolerance)) return -1;
      long i(f * (n_raw - 1));
      if (i == n_raw - 1) i--;
      return i;
    }

    bool interpolate(double given, double first, const raw* table, bool edge,
                     fpfdp& result)
    {
      if (!table) return false;
      double incr;
      if (!edge) incr = wide_incr;
      else       incr = edge_incr;
      long i = find_table_interval(given, first, incr);
      if (i < 0) return false;
      double x = (given - first) / incr - double(i);
      double fp  = table[i].fp  + x * (table[i+1].fp  - table[i].fp);
      double fdp = table[i].fdp + x * (table[i+1].fdp - table[i].fdp);
      result = fpfdp(fp, fdp);
      return true;
    }

  }}

  fpfdp Sasaki::operator()(double Energy)
  {
    fpfdp result(Efpfdp_undefined, Efpfdp_undefined);
    double given = constants::factor_eV_Angstrom / Energy;
    long i = -1;
    if (detail::sasaki::interpolate(
          given, m_info->first_k, m_info->k, true, result)) {
      return result;
    }
    if (detail::sasaki::interpolate(
          given, m_info->first_l1, m_info->l1, true, result)) {
      return result;
    }
    if (detail::sasaki::interpolate(
          given, m_info->first_l2, m_info->l2, true, result)) {
      return result;
    }
    if (detail::sasaki::interpolate(
          given, m_info->first_l3, m_info->l3, true, result)) {
      return result;
    }
    detail::sasaki::interpolate(
      given, detail::sasaki::first_wide, m_info->wide, false, result);
    return result;
  }

}} // namespace cctbx::eltbx"""

def run():
  import sys
  f = open("../reference/sasaki/fpwide.tbl", "r")
  tables_wide = collect_tables(f, 0)
  f.close()
  f = open("../reference/sasaki/fpk.tbl", "r")
  tables_k = collect_tables(f, 1)
  f.close()
  f = open("../reference/sasaki/fpl.tbl", "r")
  tables_l = collect_tables(f, 1)
  f.close()
  tables_combined = combine_tables(tables_wide, tables_k, tables_l)
  f = open("sasaki.cpp", "w")
  sys.stdout = f
  print_header()
  print_ftp_info()
  print_sasaki_cpp(tables_combined)
  f.close()
  block_size = 12
  for i_begin in xrange(0, len(tables_combined), block_size):
    i_end = min(len(tables_combined), i_begin + block_size)
    f = open("sasaki_tables_%02d_%02d.cpp" % (i_begin+1, i_end), "w")
    sys.stdout = f
    print_header()
    print_table_block(tables_combined, i_begin, i_end)
    f.close()
  sys.stdout = sys.__stdout__

if (__name__ == "__main__"):
  run()
