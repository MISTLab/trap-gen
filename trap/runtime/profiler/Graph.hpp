#ifndef GRAPH_HPP
#define GRAPH_HPP

#include <boost/graph/graph_traits.hpp>
#include <boost/graph/adjacency_list.hpp>
#include <boost/graph/filtered_graph.hpp>
#include <boost/config.hpp>

namespace resp{

struct VertexInfo{
    virtual ~VertexInfo(){}
};

struct node_info_t
{
   ///typedef defining node_info_t as vertex node
   typedef boost::vertex_property_tag kind;
};

struct edge_info_t
{
   ///typedef defining edge_info_t as edge object
   typedef boost::edge_property_tag kind;
};

///Definition of the custom property node_info.
typedef boost::property<node_info_t, VertexInfo * > node_info_property;
///Definition of the node color property. This property is required by topological_sort function.
typedef boost::property<boost::vertex_color_t, boost::default_color_type, node_info_property> Color_property ;
///Definition of the node index property. This property is required by a large set of functions.
typedef boost::property<boost::vertex_index_t, std::size_t, Color_property> Vertex_property;

typedef boost::adjacency_list<boost::listS, boost::listS, boost::bidirectionalS,  Vertex_property, 
                                                                                boost::property<edge_info_t, std::vector<double> > > Graph;

typedef boost::graph_traits<Graph>::vertex_descriptor vertex_t;
typedef boost::graph_traits<Graph>::vertex_iterator vertex_iterator;
typedef boost::graph_traits<Graph>::edge_descriptor edge_t;
typedef boost::property_map<Graph, boost::vertex_index_t>::type vertex_index_pmap_t;

class NodeWriter {
  public:
    NodeWriter(Graph &graph);
    void operator()(std::ostream& out, const vertex_t & v) const;
  private:
    Graph &graph;
    boost::property_map<Graph, node_info_t>::type nodeInfo;
};

class EdgeWriter {
  public:
    EdgeWriter(Graph &graph);
    void operator()(std::ostream& out, const edge_t & e) const;
  private:
    Graph &graph;
    boost::property_map<Graph, edge_info_t>::type edgeInfo;
};

}

#endif
