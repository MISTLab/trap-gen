#ifndef CUSTOMEXCEPTION_HPP
#define CUSTOMEXCEPTION_HPP

#include <exception>
#include <stdexcept>

class flush_exception: public runtime_error{
    flush_exception() : runtime_error(){}
    flush_exception(const char * message) : runtime_error(message){}
};

#endif
