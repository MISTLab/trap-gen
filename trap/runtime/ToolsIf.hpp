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

#include <vector>

///Base class for all the tools (profilers, debugger, etc...)
class ToolsIf{
    public:
    ///The only method which is called to activate the tool
    ///it signals to the tool that a new instruction issue has been started;
    ///the tool can then take the appropriate actions.
    ///the return value specifies whether the processor should skip
    ///the issue of the current instruction
    virtual bool newIssue() = 0;
    virtual ~ToolsIf(){}
};

class ToolsManager{
    private:
    ///List of the active tools, which are activated at every instruction
    std::vector<ToolsIf *> activeTools;
    public:
    ///Adds a tool to the list of the tool which are activated when there is a new instruction
    ///issue
    void addTool(ToolsIf &tool);
    ///The only method which is called to activate the tool
    ///it signals to the tool that a new instruction issue has been started;
    ///the tool can then take the appropriate actions.
    ///the return value specifies whether the processor should skip
    ///the issue of the current instruction
    bool newIssue();
};

#endif
