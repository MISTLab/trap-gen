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

#endif
