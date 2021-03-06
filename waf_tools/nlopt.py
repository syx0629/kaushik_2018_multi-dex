#!/usr/bin/env python
# encoding: utf-8
#| Copyright Inria May 2015
#| This project has received funding from the European Research Council (ERC) under
#| the European Union's Horizon 2020 research and innovation programme (grant
#| agreement No 637972) - see http://www.resibots.eu
#|
#| Contributor(s):
#|   - Jean-Baptiste Mouret (jean-baptiste.mouret@inria.fr)
#|   - Antoine Cully (antoinecully@gmail.com)
#|   - Kontantinos Chatzilygeroudis (konstantinos.chatzilygeroudis@inria.fr)
#|   - Federico Allocati (fede.allocati@gmail.com)
#|   - Vaios Papaspyros (b.papaspyros@gmail.com)
#|   - Roberto Rama (bertoski@gmail.com)
#|
#| This software is a computer library whose purpose is to optimize continuous,
#| black-box functions. It mainly implements Gaussian processes and Bayesian
#| optimization.
#| Main repository: http://github.com/resibots/limbo
#| Documentation: http://www.resibots.eu/limbo
#|
#| This software is governed by the CeCILL-C license under French law and
#| abiding by the rules of distribution of free software.  You can  use,
#| modify and/ or redistribute the software under the terms of the CeCILL-C
#| license as circulated by CEA, CNRS and INRIA at the following URL
#| "http://www.cecill.info".
#|
#| As a counterpart to the access to the source code and  rights to copy,
#| modify and redistribute granted by the license, users are provided only
#| with a limited warranty  and the software's author,  the holder of the
#| economic rights,  and the successive licensors  have only  limited
#| liability.
#|
#| In this respect, the user's attention is drawn to the risks associated
#| with loading,  using,  modifying and/or developing or reproducing the
#| software by the user in light of its specific status of free software,
#| that may mean  that it is complicated to manipulate,  and  that  also
#| therefore means  that it is reserved for developers  and  experienced
#| professionals having in-depth computer knowledge. Users are therefore
#| encouraged to load and test the software's suitability as regards their
#| requirements in conditions enabling the security of their systems and/or
#| data to be ensured and,  more generally, to use and operate it in the
#| same conditions as regards security.
#|
#| The fact that you are presently reading this means that you have had
#| knowledge of the CeCILL-C license and that you accept its terms.
#|
#! /usr/bin/env python
# Konstantinos Chatzilygeroudis - 2015

"""
Quick n dirty nlopt detection
"""

import os, glob, types
from waflib.Configure import conf


def options(opt):
	opt.add_option('--nlopt', type='string', help='path to nlopt', dest='nlopt')


@conf
def check_nlopt(conf):
	if conf.options.nlopt:
		includes_check = [conf.options.nlopt + '/include']
		libs_check = [conf.options.nlopt + '/lib']
	else:
		includes_check = ['/usr/local/include', '/usr/include']
		libs_check = ['/usr/local/lib', '/usr/lib', '/usr/lib/x86_64-linux-gnu/']
		if 'RESIBOTS_DIR' in os.environ:
			includes_check = [os.environ['RESIBOTS_DIR'] + '/include'] + includes_check
			libs_check = [os.environ['RESIBOTS_DIR'] + '/lib'] + libs_check

	incl = ''
	try:
		conf.start_msg('Checking for NLOpt C++ includes (optional)')
		res = conf.find_file('nlopt.hpp', includes_check)
		incl = res[:-len('nlopt.hpp')-1]
		conf.end_msg(incl)
	except:
		conf.end_msg('Not found in %s' % str(includes_check), 'YELLOW')
		return 1
	conf.start_msg('Checking for NLOpt C++ libs (optional)')
	lib_path = ''
	for lib in ['libnlopt_cxx.so', 'libnlopt_cxx.a', 'libnlopt_cxx.dylib']:
		try:
			res = conf.find_file(lib, libs_check)
			lib_path = res[:-len(lib)-1]
		except:
			continue
	if lib_path == '':
		conf.end_msg('Not found in %s' % str(libs_check), 'YELLOW')
		return 1
	else:
		conf.end_msg(lib_path)
		conf.env.INCLUDES_NLOPT = [incl]
		conf.env.LIBPATH_NLOPT = [lib_path]
		conf.env.DEFINES_NLOPT = ['USE_NLOPT']
		conf.env.LIB_NLOPT = ['nlopt_cxx']
	return 1
