#include <string>
#include <vector>
#include <iostream>
#include <iomanip>
#include <signal.h>
#include <boost/asio.hpp>
#include <boost/lexical_cast.hpp>

#include "utils.hpp"

#include "GDBConnectionManager.hpp"

using namespace resp;

GDBConnectionManager::GDBConnectionManager(bool endianess, unsigned int verbosityLevel) : endianess(endianess), killed(false), verbosityLevel(verbosityLevel){
   this->HexMap['0'] = 0;
   this->HexMap['1'] = 1;
   this->HexMap['2'] = 2;
   this->HexMap['3'] = 3;
   this->HexMap['4'] = 4;
   this->HexMap['5'] = 5;
   this->HexMap['6'] = 6;
   this->HexMap['7'] = 7;
   this->HexMap['8'] = 8;
   this->HexMap['9'] = 9;
   this->HexMap['A'] = 10;
   this->HexMap['B'] = 11;
   this->HexMap['C'] = 12;
   this->HexMap['D'] = 13;
   this->HexMap['E'] = 14;
   this->HexMap['F'] = 15;
   this->HexMap['a'] = 10;
   this->HexMap['b'] = 11;
   this->HexMap['c'] = 12;
   this->HexMap['d'] = 13;
   this->HexMap['e'] = 14;
   this->HexMap['f'] = 15;
}

GDBConnectionManager::~GDBConnectionManager(){
/*   if(this->socket != NULL && !this->killed){
      delete this->socket;
   }*/
}

///Creates a socket connection waiting on the specified port;
///this will be later used to communicate with GDB
void GDBConnectionManager::initialize(unsigned int port){
   try{
      asio::io_service io_service;
      asio::ip::tcp::acceptor acceptor(io_service, asio::ip::tcp::endpoint(asio::ip::tcp::v4(), port));

      this->socket = new asio::ip::tcp::socket(io_service);
      std::cerr << "GDB: waiting for connections on port " << port << std::endl;
      acceptor.accept(*this->socket);
      std::cerr << "GDB: connection accepted on port " << port << std::endl;
   }
   catch(...){
        this->killed = true;
        THROW_EXCEPTION("Error during the creation of the connection on port " + boost::lexical_cast<std::string>(port));        
   }
}

///Sends the response to the GDB debugger connected
void GDBConnectionManager::sendResponse(GDBResponse &response){
   //All the response packets are in the form $<packet info>#<checksum>
   #ifndef NDEBUG
   if(verbosityLevel >= 3)
        std::cerr << __PRETTY_FUNCTION__ << ": packet type " << response.type << std::endl;
   #endif

   std::string payload;
   //First of all I compute the payload; it depends on the particular packet
   //sent by GDB
   switch(response.type){
      case GDBResponse::S:{
         //S request: informs GDB that a signal interrupted program execution
         payload = 'S' + this->toHexString((unsigned char)response.payload, 2);
      break;}
      case GDBResponse::T:{
         //T request: informs GDB that a signal interrupted program execution;
         //more datailed information is provided
         payload = 'T' + this->toHexString((unsigned char)response.payload, 2);
         std::vector<std::pair<std::string, unsigned int> >::iterator pairsIter, pairsEnd;
         for(pairsIter = response.info.begin(), pairsEnd = response.info.end();
                                    pairsIter != pairsEnd; pairsIter++){
            if(pairsIter->first == "thread" || pairsIter->first == "watch" ||
            pairsIter->first == "rwatch" || pairsIter->first == "awatch" || pairsIter->first == "library"){
               //it is a hex number representing a register and the second part
               //represents the value of that register
               payload += pairsIter->first + ':' + this->toHexString(pairsIter->second, response.size*2);
            }
            else{
               //it is a hex number representing a register and the second part
               //represents the value of that register; TODO we should check that
               //this is a real number
               payload += pairsIter->first + ':' + this->toHexString(pairsIter->second, response.size*2);
            }
            payload += ';';
         }
      break;}
      case GDBResponse::W:{
         //Process Exited
         payload = 'W' + this->toHexString((unsigned char)response.payload, 2);
         this->killed = true;
      break;}
      case GDBResponse::X:{
         //Process Exited
         payload = 'X' + this->toHexString((unsigned char)response.payload);
      break;}
      case GDBResponse::OUTPUT:{
         //Sending output message to the GDB debugger console
         payload = 'O';
        std::string::iterator messageIter, messageEnd;
         for(messageIter = response.message.begin(), messageEnd = response.message.end();
                                                  messageIter != messageEnd; messageIter++){
            payload += this->toHexString((unsigned char)*messageIter, 2);
         }
      break;}
      case GDBResponse::OK:{
         payload = "OK";
      break;}
      case GDBResponse::ERROR:{
         payload = 'E' + this->toHexString((unsigned char)response.payload, 2);
      break;}
      case GDBResponse::REG_READ:
      case GDBResponse::MEM_READ:{
        std::vector<char>::iterator dataIter, dataEnd;
        for(dataIter = response.data.begin(), dataEnd = response.data.end(); dataIter != dataEnd; dataIter++)
            payload += this->toHexString((unsigned char)*dataIter, 2);
      break;}
      default:{
      break;}
   }

   unsigned char ack = '\x0';
   bool retry = false;
   do{
      //Now I complete the packet with the checksum
      std::string packet = '$' + payload + '#' + this->toHexString(this->computeChecksum(payload), 2);
   
      #ifndef NDEBUG
      if(verbosityLevel >= 1)
        std::cerr << __PRETTY_FUNCTION__ << ": Sending packet " << packet << std::endl;
      #endif
   
      //Finally I can send the packet on th network
      boost::system::error_code asioError;
      asio::write(*this->socket, asio::buffer(packet.c_str(), packet.size()), asio::transfer_all(), asioError);

      #ifndef NDEBUG
      if(asioError){
         std::cerr << __PRETTY_FUNCTION__ << ": WriteError " << asioError.message() << std::endl;
      }
      #endif
   
      //Now I have to check that the packet was correctly received, otherwise I
      //retransmitt it
      int numRestries = 0;
      retry = false;
      do{
         numRestries = 0;
          do{
              this->socket->read_some(asio::buffer(&ack, 1), asioError);
              if(asioError == asio::error::eof){
                 std::cerr << "Connection Unexpetedly closed by the GDB Debugger" << std::endl;
                 this->killed = true;
                 return;
              }
              numRestries++;
          }
          while((ack & 0x7f) != '+' && (ack & 0x7f) != '-');
          if(numRestries > 1){
            //Some random characters were received,  I signal an error
             #ifndef NDEBUG
             if(verbosityLevel >= 3)
                std::cerr << __PRETTY_FUNCTION__ << ": Sending an error since I received spurious acks" << std::endl;
             #endif

            packet = "$E00#a5";
            asio::write(*this->socket, asio::buffer(packet.c_str(), packet.size()), asio::transfer_all(), asioError);
            retry = true;
          }
      }while(numRestries > 1);
      #ifndef NDEBUG
      if(verbosityLevel >= 3)
        std::cerr << __PRETTY_FUNCTION__ << ": Received ACK " << (char)(ack & 0x7f) << " retry " << retry << std::endl;
      #endif
   }while((ack & 0x7f) == '-' || retry);
}

///Waits for the sending of a packet from GDB; it then parses it and
///translates it into the correct request
GDBRequest GDBConnectionManager::processRequest(){
   //Ok, we have to read the request and create its high level representation;
   //Note how this operation is repeated until the packet is correctly received
   std::string payload;
   bool correctlyReceived = false;
   GDBRequest req;

   do{   
      unsigned char recivedChar = '\x0';
      boost::system::error_code asioError;
   
      //Reading the starting character
      while((recivedChar & 0x7f) != '$'){
         this->socket->read_some(asio::buffer(&recivedChar, 1), asioError);
         if(asioError == asio::error::eof){
            std::cerr << "Connection Unexpetedly closed by the GDB Debugger" << std::endl;
            req.type = GDBRequest::ERROR;
            this->killed = true;
            return req;
         }
      }
      
      #ifndef NDEBUG
      if(verbosityLevel >= 3)
        std::cerr << "Received the correct message starting character" << std::endl;
      #endif
      
      //Now I have to start reading the payload: I go on until # is enocuntered;
      payload = "";
      while((recivedChar & 0x7f) != '#'){
         this->socket->read_some(asio::buffer(&recivedChar, 1), asioError);
         if(asioError == asio::error::eof){
            std::cerr << "Connection Unexpetedly closed by the GDB Debugger" << std::endl;
            req.type = GDBRequest::ERROR;
            this->killed = true;
            return req;
         }
         if((recivedChar & 0x7f) != '#')
            payload += (char)(recivedChar & 0x7f);
      }
   
      #ifndef NDEBUG
      if(verbosityLevel >= 3)
        std::cerr << "Correctly received the payload: " << payload << std::endl;
      #endif
   
      //Finally I read the checksum: it should be composed of two characters
      char checkSum[2];
      this->socket->read_some(asio::buffer(checkSum, 2), asioError);
      if(asioError == asio::error::eof){
         std::cerr << "Connection Unexpetedly closed by the GDB Debugger" << std::endl;
         req.type = GDBRequest::ERROR;
         this->killed = true;
         return req;
      }

      #ifndef NDEBUG
      if(verbosityLevel >= 3)
        std::cerr << "Received Checksum " << checkSum[0] << checkSum[1] << std::endl;
      #endif
      
      //Now I have to check the checksum...
      correctlyReceived = this->checkChecksum(payload, checkSum);
      
      //...and communicate the result of the checking to GDB server
      char checkRes;
      if(correctlyReceived){
         #ifndef NDEBUG
         if(verbosityLevel >= 3)
            std::cerr << "Checksum is Correct" << std::endl;
         #endif
         checkRes = '+';
      }
      else{
         #ifndef NDEBUG
         if(verbosityLevel >= 1)
            std::cerr << "Checksum is Wrong" << std::endl;
         #endif
         checkRes = '-';
      }
      asio::write(*this->socket, asio::buffer(&checkRes, 1), asio::transfer_all(), asioError);
      #ifndef NDEBUG
      if(asioError){
         std::cerr << __PRETTY_FUNCTION__ << ": WriteError " << asioError.message() << std::endl;
         req.type = GDBRequest::ERROR;
         return req;
      }
      #endif      
   }while(!correctlyReceived);

   #ifndef NDEBUG
   if(verbosityLevel >= 1)
    std::cerr << __PRETTY_FUNCTION__ << ": Payload correctly received " << payload << std::endl;
   #endif      
   
   //Now I have do decode the payload and transform it into the real packet
   char payType = payload[0];
   payload = payload.substr(1); 
   switch(payType){
      case '!':{
         req.type = GDBRequest::EXCL;
      break;}
      case '?':{
         req.type = GDBRequest::QUEST;
      break;}
      case 'c':{
         req.type = GDBRequest::c;
         if(payload.size() > 0){
            req.address = this->toIntNum(payload);
         }
         else
            req.address = 0;
      break;}
      case 'C':{
         req.type = GDBRequest::C;
         std::string::size_type sepIndex = payload.find(';');
         if(sepIndex == std::string::npos)
            req.signal = this->toIntNum(payload);
         else{
            std::string temp = payload.substr(0, sepIndex);
            req.signal = this->toIntNum(temp);
            temp = payload.substr(sepIndex + 1);
            req.address = this->toIntNum(temp);
         }
      break;}
      case 'D':{
         req.type = GDBRequest::D;
      break;}
      case 'g':{
         req.type = GDBRequest::g;
      break;}
      case 'G':{
         req.type = GDBRequest::G;
         std::string::iterator payIter, payIterEnd;
         for(payIter = payload.begin(), payIterEnd = payload.end();
                      payIter != payIterEnd; payIter++){
            std::string buf = "" + *payIter;
            payIter++;
            buf += *payIter;
            req.data.push_back((unsigned char)this->toIntNum(buf));
         }
      break;}
      case 'H':{
         req.type = GDBRequest::H;
         req.data.push_back(payload[0]);
         payload = payload.substr(1);
         req.value = boost::lexical_cast<int>(payload);
      break;}
      case 'i':{
         req.type = GDBRequest::i;
         if(payload.size() > 0){
            std::string::size_type sepIndex = payload.find(',');
            if(sepIndex == std::string::npos){
               req.value = 1;
               req.address = this->toIntNum(payload);
            }
            else{
               std::string temp = payload.substr(0, sepIndex);
               req.address = this->toIntNum(temp);
               temp = payload.substr(sepIndex + 1);
               req.value = this->toIntNum(temp);
            }
         }
         else{
            req.address = 0;
            req.value = 1;
         }
      break;}
      case 'I':{
         req.type = GDBRequest::I;
      break;}
      case 'k':{
         this->killed = true;
         req.type = GDBRequest::k;
      break;}
      case 'm':{
         req.type = GDBRequest::m;
         std::string::size_type sepIndex = payload.find(',');
         #ifndef NDEBUG
         if(sepIndex == std::string::npos)
            std::cerr << __PRETTY_FUNCTION__ << ": error in the m message: no arguments given" << std::endl;
         #endif
         std::string temp = payload.substr(0, sepIndex);
         req.address = this->toIntNum(temp);
         temp = payload.substr(sepIndex + 1);
         req.length = this->toIntNum(temp);         
      break;}
      case 'M':{
         req.type = GDBRequest::M;
         std::string::size_type sepIndex = payload.find(',');
         std::string::size_type sepIndex2 = payload.find(':');
         #ifndef NDEBUG
         if(sepIndex == std::string::npos || sepIndex2 == std::string::npos)
            std::cerr << __PRETTY_FUNCTION__ << ": error in the M message: no arguments given" << std::endl;
         #endif
         std::string temp = payload.substr(0, sepIndex);
         req.address = this->toIntNum(temp);
         temp = payload.substr(sepIndex + 1, sepIndex2 - sepIndex - 1);
         req.length = this->toIntNum(temp);
         temp = payload.substr(sepIndex2 + 1);
         //Now it is time to read the content of memory
         std::string::iterator dataIter, dataIterEnd;
         for(dataIter = temp.begin(), dataIterEnd = temp.end(); dataIter != dataIterEnd; dataIter++){
            std::string buf = "" + *dataIter;
            dataIter++;
            buf += *dataIter;
            req.data.push_back((unsigned char)this->toIntNum(buf));
         }
         //Now I check that the length of the buffer is the specified one
         #ifndef NDEBUG
         if(req.data.size() != req.length)
           std::cerr << __PRETTY_FUNCTION__ << ": error in the M message: different length of bytes" << std::endl;
         #endif
      break;}
      case 'p':{
         req.type = GDBRequest::p;
         req.reg = this->toIntNum(payload);
      break;}
      case 'P':{
         req.type = GDBRequest::P;
         std::string::size_type sepIndex = payload.find('=');
         #ifndef NDEBUG
         if(sepIndex == std::string::npos)
            std::cerr << __PRETTY_FUNCTION__ << ": error in the P message: no arguments given" << std::endl;
         #endif
         std::string temp = payload.substr(0, sepIndex);
         req.reg = this->toIntNum(temp);
         temp = payload.substr(sepIndex + 1);
         req.value = this->toIntNum(temp);
      break;}
      case 'q':{
         req.type = GDBRequest::q;
         std::string::size_type sepIndex = payload.find(',');
         if(sepIndex == std::string::npos){
             #ifndef NDEBUG
             if(verbosityLevel >= 1)
                std::cerr << __PRETTY_FUNCTION__ << ": q message payload " << payload << std::endl;
             #endif
            req.type = GDBRequest::UNK;
            break;
         }
         std::string temp = payload.substr(0, sepIndex);
         req.command = temp;
         temp = payload.substr(sepIndex + 1);
         req.extension = this->toStr(temp);
      break;}
      case 's':{
         req.type = GDBRequest::s;
         if(payload.size() > 0)
            req.address = this->toIntNum(payload);
         else
            req.address = 0; 
      break;}
      case 'S':{
         req.type = GDBRequest::S;
         std::string::size_type sepIndex = payload.find(';');
         if(sepIndex == std::string::npos)
            req.signal = this->toIntNum(payload);
         else{
            std::string temp = payload.substr(0, sepIndex);
            req.signal = this->toIntNum(temp);
            temp = payload.substr(sepIndex + 1);
            req.address = this->toIntNum(temp);
         }
      break;}
      case 't':{
         req.type = GDBRequest::t;
         std::string::size_type sepIndex = payload.find(':');
         std::string::size_type sepIndex2 = payload.find(',');
         #ifndef NDEBUG
         if(sepIndex == std::string::npos || sepIndex2 == std::string::npos)
            std::cerr << __PRETTY_FUNCTION__ << ": error in the t message: no arguments given" << std::endl;
         #endif
         std::string temp = payload.substr(0, sepIndex);
         req.address = this->toIntNum(temp);
         temp = payload.substr(sepIndex + 1, sepIndex2 - sepIndex - 1);
         req.value = this->toIntNum(temp);
         temp = payload.substr(sepIndex2 + 1);
         req.length = this->toIntNum(temp);
      break;}
      case 'T':{
         req.type = GDBRequest::T;
         req.value = this->toIntNum(payload);
      break;}
      case 'X':{
         req.type = GDBRequest::X;
         std::string::size_type sepIndex = payload.find(',');
         std::string::size_type sepIndex2 = payload.find(':');
         #ifndef NDEBUG
         if(sepIndex == std::string::npos || sepIndex2 == std::string::npos)
            std::cerr << __PRETTY_FUNCTION__ << ": error in the M message: no arguments given" << std::endl;
         #endif
         std::string temp = payload.substr(0, sepIndex);
         req.address = this->toIntNum(temp);
         temp = payload.substr(sepIndex + 1, sepIndex2 - sepIndex - 1);
         req.length = this->toIntNum(temp);
         temp = payload.substr(sepIndex2 + 1);
         //Now it is time to read the content of memory
         std::string::iterator dataIter, dataIterEnd;
         for(dataIter = temp.begin(), dataIterEnd = temp.end(); dataIter != dataIterEnd; dataIter++){
            req.data.push_back(*dataIter);
         }
         //Now I check that the length of the buffer is the specified one
         #ifndef NDEBUG
         if(req.data.size() != req.length)
           std::cerr << __PRETTY_FUNCTION__ << ": error in the X message: different length of bytes" << std::endl;
         #endif
      break;}
      case 'z':{
         req.type = GDBRequest::z;
         std::string::size_type sepIndex = payload.find(',');
         std::string::size_type sepIndex2 = payload.find_last_of(',');
         #ifndef NDEBUG
         if(sepIndex == std::string::npos || sepIndex2 == std::string::npos)
            std::cerr << __PRETTY_FUNCTION__ << ": error in the z message: no arguments given" << std::endl;
         #endif
         std::string temp = payload.substr(0, sepIndex);
         req.value = this->toIntNum(temp);
         temp = payload.substr(sepIndex + 1, sepIndex2 - sepIndex - 1);
         req.address = this->toIntNum(temp);
         temp = payload.substr(sepIndex2 + 1);
         req.length = this->toIntNum(temp);
      break;}
      case 'Z':{
         req.type = GDBRequest::Z;
         std::string::size_type sepIndex = payload.find(',');
         std::string::size_type sepIndex2 = payload.find_last_of(',');
         #ifndef NDEBUG
         if(sepIndex == std::string::npos || sepIndex2 == std::string::npos)
            std::cerr << __PRETTY_FUNCTION__ << ": error in the Z message: no arguments given" << std::endl;
         #endif
         std::string temp = payload.substr(0, sepIndex);
         req.value = this->toIntNum(temp);
         temp = payload.substr(sepIndex + 1, sepIndex2 - sepIndex - 1);
         req.address = this->toIntNum(temp);
         temp = payload.substr(sepIndex2 + 1);
         req.length = this->toIntNum(temp);
      break;}
      default:{
         req.type = GDBRequest::UNK;
      break;}
   }
   
   return req;
}

///Sends and interrupt message to the GDB debugger signaling that
///the execution of the program halted: this way the GDB
///debugger becomes responsive and it is possible to debug the
///program under test
void GDBConnectionManager::sendInterrupt(){
   GDBResponse response;
   response.type = GDBResponse::S;
   response.payload = SIGTRAP;
   
   this->sendResponse(response);
}

///Closes the connection with the GDB debugger
void GDBConnectionManager::disconnect(){
   if(this->socket != NULL){
      if(this->socket->is_open())
         this->socket->close();
      delete this->socket;
      this->socket = NULL;
   }
}

///Computes the checksum for the data
unsigned char GDBConnectionManager::computeChecksum(std::string &data){
   unsigned char sum = 0;
   std::string::iterator dataIter, dataEnd;
   for(dataIter = data.begin(), dataEnd = data.end(); dataIter != dataEnd; dataIter++)
      sum += (unsigned char)*dataIter;
   return sum;
}

///Checks that the checksum included in the packet is correct
bool GDBConnectionManager::checkChecksum(std::string &data, char checkSum[2]){
   unsigned char compCheck = this->computeChecksum(data);
   #ifndef NDEBUG
   if(verbosityLevel >= 3)
      std::cerr << __PRETTY_FUNCTION__ << ": Computed CheckSum " << (unsigned int)compCheck << std::endl;
   #endif

   //std::string hexCheckSum = "" + checkSum[0] + checkSum[1];
   unsigned char recvCheck = ((this->chToHex(checkSum[0]) & 0x0f) << 4) | (this->chToHex(checkSum[1]) & 0x0f);
   #ifndef NDEBUG
   if(verbosityLevel >= 3)
       std::cerr << __PRETTY_FUNCTION__ << ": Received CheckSum " << (unsigned int)recvCheck << std::endl;
   #endif   
   
   return compCheck == recvCheck;
}

///Converts a generic numeric value into a string of hex numbers;
///each hew number of the string is in the same order of the endianess
///of the processor linked to this stub 
std::string GDBConnectionManager::toHexString(unsigned int value, int numChars){
   std::ostringstream os;

   #ifndef NDEBUG
   if(verbosityLevel >= 3)
      std::cerr << __PRETTY_FUNCTION__ << ": Converting " << std::hex << value << std::dec << std::endl;
   #endif
   
   if(this->endianess && ((value & 0xFFFFFF00) != 0)){
      //I have to flip the bytes of value so that the endianess is correct
      value = ((value & 0x000000FF) << 24) | ((value & 0x0000FF00) << 8) | 
                ((value & 0x00FF0000) >> 8) | ((value & 0xFF000000) >> 24);
       #ifndef NDEBUG
       if(verbosityLevel >= 3)
          std::cerr << __PRETTY_FUNCTION__ << ": Value after endianess convertion " << std::hex << value << std::dec << std::endl;
       #endif
   }
   
   //Conversion to hex
   if(numChars == -1)
      os << std::hex << value;
   else
      os << std::hex << std::setw(numChars) << std::setfill('0') << value;
   
   return os.str();
}

///Converts an hexadecimal number expressed with a string
///into its correspondent integer number
///each hex number of the string is in the same order of the endianess
///of the processor linked to this stub 
unsigned int GDBConnectionManager::toIntNum(std::string &toConvert){
   #ifndef NDEBUG
   if(verbosityLevel >= 3)
      std::cerr << __PRETTY_FUNCTION__ << ": Converting " << toConvert << std::endl;
   #endif

   std::string toConvTemp = toConvert;
   if(toConvTemp.size() >= 2 && toConvTemp[0] == '0' && (toConvTemp[1] == 'X' || toConvTemp[1] == 'x')) 
      toConvTemp = toConvTemp.substr(2);

   unsigned int result = 0;
   unsigned int pos = 0;
   std::string::reverse_iterator hexIter, hexIterEnd;
   for(hexIter = toConvTemp.rbegin(), hexIterEnd = toConvTemp.rend();
                  hexIter != hexIterEnd; hexIter++){
      std::map<char, unsigned int>::iterator mapIter = this->HexMap.find(*hexIter);
      #ifndef NDEBUG
      if(mapIter == this->HexMap.end()){
         std::cerr << __PRETTY_FUNCTION__ << ": bad hex convertion; trying to cast 0x" << toConvTemp << " current character -" << *hexIter << "-" << std::endl;
         return 0;
      }
      #endif
      result |= (mapIter->second << pos);
      pos += 4;
   }
   
//   if(this->endianess && (result & 0xFFFFFF00) != 0){
//      //I have to flip the bytes of value so that the endianess is correct
//      result = ((result & 0x000000FF) << 24) | ((result & 0x0000FF00) << 8) | 
//                ((result & 0x00FF0000) >> 8) | ((result & 0xFF000000) >> 24);
//   }
   
   #ifndef NDEBUG
   if(verbosityLevel >= 3)
       std::cerr << __PRETTY_FUNCTION__ << ": converted " << result << std::endl;
   #endif
   
   return result;
}

///Converts a hex character to an int representing it
int GDBConnectionManager::chToHex(unsigned char ch){
   if(ch >= 'a' && ch <= 'f')
      return ch-'a'+10;
   if(ch >= '0' && ch <= '9')
      return ch-'0';
   if(ch >= 'A' && ch <= 'F')
      return ch-'A'+10;
   return -1;
}

///Converts a hexadecimal number into the corresponding character string
std::string GDBConnectionManager::toStr(std::string &toConvert){
    //What I do is to read the string element in couples; then
    //I convert each couple to its integer representation:
    //that is one string character
    #ifndef NDEBUG
   if(verbosityLevel >= 3)
       std::cerr << __PRETTY_FUNCTION__ << ": converting " << toConvert << std::endl;
    #endif
    #ifndef NDEBUG
    if((toConvert.size() % 2) != 0){
         std::cerr << __PRETTY_FUNCTION__ << ": hexadecimal string contains an odd ammount of characters " << toConvert << std::endl;
         return "";
     }
    #endif
    std::string outMex = "";
    for(unsigned int i = 0; i < toConvert.size()/2; i++){
         std::string temp = toConvert.substr(i*2,  2);
         outMex += (char)(this->toIntNum(temp));
    }
    
    #ifndef NDEBUG
   if(verbosityLevel >= 3)
       std::cerr << __PRETTY_FUNCTION__ << ": converted " << outMex << std::endl;
    #endif
    
    return outMex;
}
