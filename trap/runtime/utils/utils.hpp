/***************************************************************************\
 *
 *
 *            ___        ___           ___           ___
 *           /  /\      /  /\         /  /\         /  /\
 *          /  /:/     /  /::\       /  /::\       /  /::\
 *         /  /:/     /  /:/\:\     /  /:/\:\     /  /:/\:\
 *        /  /:/     /  /:/~/:/    /  /:/~/::\   /  /:/~/:/
 *       /  /::\    /__/:/ /:/___ /__/:/ /:/\:\ /__/:/ /:/
 *      /__/:/\:\   \  \:\/:::::/ \  \:\/:/__\/ \  \:\/:/
 *      \__\/  \:\   \  \::/~~~~   \  \::/       \  \::/
 *           \  \:\   \  \:\        \  \:\        \  \:\
 *            \  \ \   \  \:\        \  \:\        \  \:\
 *             \__\/    \__\/         \__\/         \__\/
 *
 *
 *
 *
 *   This file is part of TRAP.
 *
 *   TRAP is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU Lesser General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU Lesser General Public License for more details.
 *
 *   You should have received a copy of the GNU Lesser General Public License
 *   along with this program; if not, write to the
 *   Free Software Foundation, Inc.,
 *   51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 *   or see <http://www.gnu.org/licenses/>.
 *
 *
 *
 *   (c) Luca Fossati, fossati@elet.polimi.it
 *
\***************************************************************************/

#ifndef UTILS_HPP
#define UTILS_HPP

#include <string>
#include <iostream>
#include <sstream>
#include <exception>
#include <stdexcept>

#ifdef MAKE_STRING
#undef MAKE_STRING
#endif
#define MAKE_STRING( msg )  ( ((std::ostringstream&)((std::ostringstream() << '\x0') << msg)).str().substr(1) )

#ifdef THROW_EXCEPTION
#undef THROW_EXCEPTION
#endif
#define THROW_EXCEPTION( msg ) ( throw std::runtime_error(MAKE_STRING( "At: function " << __PRETTY_FUNCTION__ << " file: " << __FILE__ << ":" << __LINE__ << " --> " << msg )) )

#ifdef THROW_ERROR
#undef THROW_ERROR
#endif
#define THROW_ERROR( msg ) ( {std::cerr << "At: function " << __PRETTY_FUNCTION__ << " file: " << __FILE__ << ":" << __LINE__ << " --> " << msg << std::endl;exit(0);} )

#endif
