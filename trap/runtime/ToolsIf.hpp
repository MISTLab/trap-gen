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

#ifndef TOOLSIF_HPP
#define TOOLSIF_HPP

#include <cstdlib>

namespace trap{

///Base class for the tools which need to interact with memory,
///i.e. to be called for every write operation which happens in
///memory. Note that only one tool at a time can interact
///with memory
template<class addressType> class MemoryToolsIf{
    public:
    #ifndef NDEBUG
    virtual void notifyAddress(addressType address, unsigned int size) throw() = 0;
    #else
    virtual void notifyAddress(addressType address, unsigned int size) = 0;
    #endif
    virtual ~MemoryToolsIf(){}
};

///Base class for all the tools (profilers, debugger, etc...)
template<class issueWidth> class ToolsIf{
    public:
    ///The only method which is called to activate the tool
    ///it signals to the tool that a new instruction issue has been started;
    ///the tool can then take the appropriate actions.
    ///the return value specifies whether the processor should skip
    ///the issue of the current instruction
    virtual bool newIssue(const issueWidth &curPC, const void *curInstr) throw() = 0;
    virtual ~ToolsIf(){}
};

template<class issueWidth> class ToolsManager{
    private:
    ///List of the active tools, which are activated at every instruction
    ToolsIf<issueWidth> ** activeTools;
    int activeToolsNum;
    public:
    ToolsManager(){
        activeTools = NULL;
        activeToolsNum = 0;
    }
    ///Adds a tool to the list of the tool which are activated when there is a new instruction
    ///issue
    void addTool(ToolsIf<issueWidth> &tool){
        this->activeToolsNum++;
        ToolsIf<issueWidth> ** activeToolsTemp = new ToolsIf<issueWidth> *[activeToolsNum];
        if(this->activeTools != NULL){
            for(int i = 0; i < (this->activeToolsNum - 1); i++){
                activeToolsTemp[i] = this->activeTools[i];
            }
            delete [] this->activeTools;
        }
        this->activeTools = activeToolsTemp;
        this->activeTools[this->activeToolsNum - 1] = &tool;
    }
    ///The only method which is called to activate the tool
    ///it signals to the tool that a new instruction issue has been started;
    ///the tool can then take the appropriate actions.
    ///the return value specifies whether the processor should skip
    ///the issue of the current instruction
    inline bool newIssue(const issueWidth &curPC, const void *curInstr) const throw(){
        bool skipInstruction = false;
        for(int i = 0; i < this->activeToolsNum; i++){
            skipInstruction |= this->activeTools[i]->newIssue(curPC, curInstr);
        }
        return skipInstruction;
    }
};

};

#endif
