#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/filtered_graph.hpp>
#include <boost/config.hpp>

#include "Graph.hpp"
#include "profiler.hpp"

using namespace resp;

NodeWriter::NodeWriter(Graph &graph) : graph(graph){
    this->nodeInfo = boost::get(node_info_t(), this->graph);
}

void NodeWriter::operator()(std::ostream& out, const vertex_t & v) const {
    Function * fun = dynamic_cast<Function *>(this->nodeInfo[v]);
    out << "[label=\"" << fun->name << "\"]";
}

EdgeWriter::EdgeWriter(Graph &graph) : graph(graph){
    this->edgeInfo = boost::get(edge_info_t(), this->graph);
}

void EdgeWriter::operator()(std::ostream& out, const edge_t & e) const {
    const std::vector<double> &times = this->edgeInfo[e];
    out << "[label=\"";
    if(times.size() > 2)
        out << "too may calls";
    else{
        std::vector<double>::const_iterator iter,  iterEnd;
        for(iter = times.begin(),  iterEnd = times.end(); iter !=  iterEnd; iter++){
            out << *iter << " - ";
        }
    }
    out << "\"]";
}
