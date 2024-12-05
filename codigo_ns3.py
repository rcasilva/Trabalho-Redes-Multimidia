/**
 * Programa derivado do tutorial "sixth.cc" do NS3.
 * Feitas modificações para acomodar a proposta do trabalho.
 * Trabalha em conjunto com classes disponibilizadas para tutorial.
 */

#include "tutorial-app.h"
#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"
#include <fstream>

using namespace ns3;

const double BACKGROUND_START_TIME = 1.0;
const double BACKGROUND_END_TIME = 300.0;

NS_LOG_COMPONENT_DEFINE("Trabalho de Computacao Movel");

/**
 * Congestion window change callback
 *
 * \param stream The output stream file.
 * \param oldCwnd Old congestion window.
 * \param newCwnd New congestion window.
 */
static void
CwndChange(Ptr<OutputStreamWrapper> stream, uint32_t oldCwnd, uint32_t newCwnd)
{
    //NS_LOG_UNCOND("CWND change at " << Simulator::Now().GetSeconds() << " to " << newCwnd);
    *stream->GetStream() << Simulator::Now().GetSeconds() << "\t" << oldCwnd << "\t" << newCwnd
                         << std::endl;
}

/**
 * Rx drop callback
 *
 * \param file The output PCAP file.
 * \param p The dropped packet.
 */
static void
RxDrop(Ptr<PcapFileWrapper> file, Ptr<const Packet> p)
{
    Ptr<Packet> copy = p->Copy();

    PppHeader pppHeader;
    copy->RemoveHeader(pppHeader);
    Ipv4Header ipHeader;
    copy->RemoveHeader(ipHeader);
    /*NS_LOG_UNCOND("RxDrop at " << Simulator::Now().GetSeconds() <<
                  " src: " << ipHeader.GetSource() <<
                  " dst: " << ipHeader.GetDestination());*/
    file->Write(Simulator::Now(), p);
}

/**
 * Callback de pacote enviado
 * 
 * \param stream Arquivo de saída.
 * \param p Pacote enviado.
 */
static void
TxPacketDone(Ptr<OutputStreamWrapper> stream, Ptr<const Packet> p)
{
    // Copio o pacote e extraio os cabeçalhos.
    Ptr<Packet> copy = p->Copy();
    PppHeader pppHeader;
    copy->RemoveHeader(pppHeader);
    Ipv4Header ipHeader;
    copy->RemoveHeader(ipHeader);
    TcpHeader tcpHeader;
    copy->RemoveHeader(tcpHeader);

    // Log no terminal.
    /*
    NS_LOG_UNCOND("ENVIADO at " << Simulator::Now().GetSeconds() <<
                  //" src: " << ipHeader.GetSource() <<
                  //" dst: " << ipHeader.GetDestination() <<
                  " seqnum: " << tcpHeader.GetSequenceNumber());*/

    // Log em arquivo.
    *stream->GetStream() << Simulator::Now().GetSeconds() << std::endl;
}

/**
 * Callback de pacote recebido
 * 
 * \param stream Arquivo de saída.
 * \param p Pacote enviado.
 */
static void
RxPacketDone(Ptr<OutputStreamWrapper> stream, Ptr<const Packet> p)
{
    // Copio o pacote e extraio os cabeçalhos.
    Ptr<Packet> copy = p->Copy();
    PppHeader pppHeader;
    copy->RemoveHeader(pppHeader);
    Ipv4Header ipHeader;
    copy->RemoveHeader(ipHeader);
    TcpHeader tcpHeader;
    copy->RemoveHeader(tcpHeader);

    // Log no terminal.
    /*
    NS_LOG_UNCOND("RECEBIDO at " << Simulator::Now().GetSeconds() <<
                  //" src: " << ipHeader.GetSource() <<
                  //" dst: " << ipHeader.GetDestination() <<
                  " seqnum: " << tcpHeader.GetSequenceNumber());*/

    // Log em arquivo.
    *stream->GetStream() << Simulator::Now().GetSeconds() << std::endl;
}

int
main(int argc, char* argv[])
{
    CommandLine cmd(__FILE__);
    cmd.Parse(argc, argv);

    // Nodes 0 e 1 são os roteadores.
    // Os próximos n/2 nodes são clientes conectados ao roteador 0.
    // Os n/2 nodes restantes são servidores conectados ao roteador 1.
    NS_LOG_INFO ("Criando os nodes...");
    Ptr<Node> r1 = CreateObject<Node>();
    Ptr<Node> r2 = CreateObject<Node>();
    Ptr<Node> cli1 = CreateObject<Node>();
    Ptr<Node> cli2 = CreateObject<Node>();
    Ptr<Node> cli3 = CreateObject<Node>();
    Ptr<Node> cli4 = CreateObject<Node>();
    Ptr<Node> cli5 = CreateObject<Node>();
    Ptr<Node> cli6 = CreateObject<Node>();
    Ptr<Node> cli7 = CreateObject<Node>();
    Ptr<Node> cli8 = CreateObject<Node>();
    Ptr<Node> cli9 = CreateObject<Node>();
    Ptr<Node> cli10 = CreateObject<Node>();
    Ptr<Node> srv1 = CreateObject<Node>();
    Ptr<Node> srv2 = CreateObject<Node>();
    Ptr<Node> srv3 = CreateObject<Node>();
    Ptr<Node> srv4 = CreateObject<Node>();
    Ptr<Node> srv5 = CreateObject<Node>();
    Ptr<Node> srv6 = CreateObject<Node>();
    Ptr<Node> srv7 = CreateObject<Node>();
    Ptr<Node> srv8 = CreateObject<Node>();
    Ptr<Node> srv9 = CreateObject<Node>();
    Ptr<Node> srv10 = CreateObject<Node>();

    // Container com todos os nodes.
    NodeContainer c;
    c = NodeContainer (r1, r2,
                       cli1, cli2, cli3, cli4, cli5, cli6, cli7, cli8, cli9, cli10,
                       srv1, srv2, srv3, srv4, srv5, srv6, srv7, srv8, srv9, srv10);

    // Instalando internet stack.
    NS_LOG_INFO ("Instalando \"internet\" nos nodes...");
    InternetStackHelper stack;
    stack.Install(c);

    // Criando os canais ponto a ponto entre r1/clientes e r2/servidores
    NS_LOG_INFO ("Criando canais de comunicação p2p...");
    PointToPointHelper p2p;

    // Canais de 10Mbit, com propagação de 1ms.
    p2p.SetDeviceAttribute ("DataRate", StringValue ("10Mbps"));
    p2p.SetChannelAttribute ("Delay", StringValue ("3ms"));
    //p2p.SetQueue("ns3::DropTailQueue", "MaxSize", StringValue("10p"));
    
    // Containers com as interfaces ponto a ponto.
    // O índice 0 sempre se refere a um dos roteadores.
    // O índice 1 sempre se refere a um dos clientes ou um dos servidores.
    NetDeviceContainer ndc_r1_r2 = p2p.Install(r1,r2);
    NetDeviceContainer ndc_r1_cli1 = p2p.Install(r1,cli1);
    NetDeviceContainer ndc_r1_cli2 = p2p.Install(r1,cli2);
    NetDeviceContainer ndc_r1_cli3 = p2p.Install(r1,cli3);
    NetDeviceContainer ndc_r1_cli4 = p2p.Install(r1,cli4);
    NetDeviceContainer ndc_r1_cli5 = p2p.Install(r1,cli5);
    NetDeviceContainer ndc_r1_cli6 = p2p.Install(r1,cli6);
    NetDeviceContainer ndc_r1_cli7 = p2p.Install(r1,cli7);
    NetDeviceContainer ndc_r1_cli8 = p2p.Install(r1,cli8);
    NetDeviceContainer ndc_r1_cli9 = p2p.Install(r1,cli9);
    NetDeviceContainer ndc_r1_cli10 = p2p.Install(r1,cli10);
    NetDeviceContainer ndc_r2_srv1 = p2p.Install(r2,srv1);
    NetDeviceContainer ndc_r2_srv2 = p2p.Install(r2,srv2);
    NetDeviceContainer ndc_r2_srv3 = p2p.Install(r2,srv3);
    NetDeviceContainer ndc_r2_srv4 = p2p.Install(r2,srv4);
    NetDeviceContainer ndc_r2_srv5 = p2p.Install(r2,srv5);
    NetDeviceContainer ndc_r2_srv6 = p2p.Install(r2,srv6);
    NetDeviceContainer ndc_r2_srv7 = p2p.Install(r2,srv7);
    NetDeviceContainer ndc_r2_srv8 = p2p.Install(r2,srv8);
    NetDeviceContainer ndc_r2_srv9 = p2p.Install(r2,srv9);
    NetDeviceContainer ndc_r2_srv10 = p2p.Install(r2,srv10);

    // Alocando IPv4 /30 para cada ponto a ponto.
    // O primeiro IP livre do /30 sempre fica com o roteador.
    // O segundo IP livre do /30 sempre fica com o cliente ou servidor.
    NS_LOG_INFO ("Alocando IPs...");
    Ipv4AddressHelper ipv4;
    ipv4.SetBase ("10.0.0.0", "255.255.255.252");
    Ipv4InterfaceContainer ic_r1_r2 = ipv4.Assign(ndc_r1_r2);
    ipv4.SetBase ("10.0.0.4", "255.255.255.252");
    Ipv4InterfaceContainer ic_r1_cli1 = ipv4.Assign(ndc_r1_cli1);
    ipv4.SetBase ("10.0.0.8", "255.255.255.252");
    Ipv4InterfaceContainer ic_r1_cli2 = ipv4.Assign(ndc_r1_cli2);
    ipv4.SetBase ("10.0.0.12", "255.255.255.252");
    Ipv4InterfaceContainer ic_r1_cli3 = ipv4.Assign(ndc_r1_cli3);
    ipv4.SetBase ("10.0.0.16", "255.255.255.252");
    Ipv4InterfaceContainer ic_r1_cli4 = ipv4.Assign(ndc_r1_cli4);
    ipv4.SetBase ("10.0.0.20", "255.255.255.252");
    Ipv4InterfaceContainer ic_r1_cli5 = ipv4.Assign(ndc_r1_cli5);
    ipv4.SetBase ("10.0.0.24", "255.255.255.252");
    Ipv4InterfaceContainer ic_r1_cli6 = ipv4.Assign(ndc_r1_cli6);
    ipv4.SetBase ("10.0.0.28", "255.255.255.252");
    Ipv4InterfaceContainer ic_r1_cli7 = ipv4.Assign(ndc_r1_cli7);
    ipv4.SetBase ("10.0.0.32", "255.255.255.252");
    Ipv4InterfaceContainer ic_r1_cli8 = ipv4.Assign(ndc_r1_cli8);
    ipv4.SetBase ("10.0.0.36", "255.255.255.252");
    Ipv4InterfaceContainer ic_r1_cli9 = ipv4.Assign(ndc_r1_cli9);
    ipv4.SetBase ("10.0.0.40", "255.255.255.252");
    Ipv4InterfaceContainer ic_r1_cli10 = ipv4.Assign(ndc_r1_cli10);
    ipv4.SetBase ("10.0.0.44", "255.255.255.252");
    Ipv4InterfaceContainer ic_r2_srv1 = ipv4.Assign(ndc_r2_srv1);
    ipv4.SetBase ("10.0.0.48", "255.255.255.252");
    Ipv4InterfaceContainer ic_r2_srv2 = ipv4.Assign(ndc_r2_srv2);
    ipv4.SetBase ("10.0.0.52", "255.255.255.252");
    Ipv4InterfaceContainer ic_r2_srv3 = ipv4.Assign(ndc_r2_srv3);
    ipv4.SetBase ("10.0.0.56", "255.255.255.252");
    Ipv4InterfaceContainer ic_r2_srv4 = ipv4.Assign(ndc_r2_srv4);
    ipv4.SetBase ("10.0.0.60", "255.255.255.252");
    Ipv4InterfaceContainer ic_r2_srv5 = ipv4.Assign(ndc_r2_srv5);
    ipv4.SetBase ("10.0.0.64", "255.255.255.252");
    Ipv4InterfaceContainer ic_r2_srv6 = ipv4.Assign(ndc_r2_srv6);
    ipv4.SetBase ("10.0.0.68", "255.255.255.252");
    Ipv4InterfaceContainer ic_r2_srv7 = ipv4.Assign(ndc_r2_srv7);
    ipv4.SetBase ("10.0.0.72", "255.255.255.252");
    Ipv4InterfaceContainer ic_r2_srv8 = ipv4.Assign(ndc_r2_srv8);
    ipv4.SetBase ("10.0.0.76", "255.255.255.252");
    Ipv4InterfaceContainer ic_r2_srv9 = ipv4.Assign(ndc_r2_srv9);
    ipv4.SetBase ("10.0.0.80", "255.255.255.252");
    Ipv4InterfaceContainer ic_r2_srv10 = ipv4.Assign(ndc_r2_srv10);

    // Populando tabelas de roteamento.
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    // Criando aplicações onoff para tráfego UDP
    NS_LOG_INFO ("Criando aplicações UDP...");
    uint16_t port = 9;
    
    // Fluxos UDP. Modelar a internet é praticamente impossível, por haver sazonalidade,
    // perfis de usuário, perfis de rede e afins.
    // Os dados abaixo são um chute mais ou menos na direção do esperado de ISP que
    // atende clientes residenciais. Dados extraídos do agregado de quatro ISPs do RJ.
    // Os fluxos aqui são 2x maiores que o esperado, pois depois será aplicado um modelo
    // de perda de 50% sobre eles, de forma a trazer alguma "imprevisibilidade".

    // Flow1: aproxima META (~15% do tráfego UDP da internet,
    // pacotes udp/quic, tamanho 1260 (1230 payload + 30 overhead))
    OnOffHelper flow1 ("ns3::UdpSocketFactory",
                       Address (InetSocketAddress (ic_r1_cli1.GetAddress (1), port)));
    flow1.SetConstantRate(DataRate("2000000b/s"), uint32_t (1230));

    // Flow 2: aproxima Google/Youtube (~16% do tráfego UDP da internet,
    // pacotes udp/quic pra youtube e google, tamanho 1278 (1248 payload + 30 overhead))
    OnOffHelper flow2 ("ns3::UdpSocketFactory",
                       Address (InetSocketAddress (ic_r1_cli2.GetAddress (1), port)));
    flow2.SetConstantRate(DataRate("2000000b/s"), int32_t (1248));

    // Flow 3: aproxima quaisquer outros fluxos "grandes" em pacotes
    // tamanho 1400 (1370 payload + 30 overhead)
    OnOffHelper flow3 ("ns3::UdpSocketFactory",
                       Address (InetSocketAddress (ic_r1_cli3.GetAddress (1), port)));
    flow3.SetConstantRate(DataRate("2000000b/s"), int32_t (1370));

    // Flow 4: aproxima pacotes de tamanho intermediário (próximo dos 512 bytes)
    // tamanho 530 (500 payload + 30 overhead)
    OnOffHelper flow4 ("ns3::UdpSocketFactory",
                       Address (InetSocketAddress (ic_r1_cli4.GetAddress (1), port)));
    flow4.SetConstantRate(DataRate("2000000b/s"), int32_t (500));

    // Flow 5: aproxima pacotes pequenos (ex.: DNS)
    // tamanho 94 (64 payload + 30 overhead)
    OnOffHelper flow5 ("ns3::UdpSocketFactory",
                       Address (InetSocketAddress (ic_r1_cli5.GetAddress (1), port)));
    flow5.SetConstantRate(DataRate("2000000b/s"), int32_t (64));

    // Flow 6: aproxima pacotes grandes (referência: scrubbing no Prime Video)
    // tamanho 1308 (1288 payload + 30 overhead)
    OnOffHelper flow6 ("ns3::UdpSocketFactory",
                       Address (InetSocketAddress (ic_r1_cli6.GetAddress (1), port)));
    flow6.SetConstantRate(DataRate("2000000b/s"), int32_t (1288));

    ApplicationContainer udpApp1;
    ApplicationContainer udpApp2;
    ApplicationContainer udpApp3;
    ApplicationContainer udpApp4;
    ApplicationContainer udpApp5;
    ApplicationContainer udpApp6;
    udpApp1.Add (flow1.Install(srv1));
    udpApp2.Add (flow2.Install(srv2));
    udpApp3.Add (flow3.Install(srv3));
    udpApp4.Add (flow4.Install(srv4));
    udpApp5.Add (flow5.Install(srv5));
    udpApp6.Add (flow6.Install(srv6));

    NS_LOG_INFO ("Criando sinks UDP...");
    PacketSinkHelper sink1 ("ns3::UdpSocketFactory",
                            Address (InetSocketAddress (Ipv4Address::GetAny (), port)));
    
    PacketSinkHelper sink2 ("ns3::UdpSocketFactory",
                            Address (InetSocketAddress (Ipv4Address::GetAny (), port)));
    
    PacketSinkHelper sink3 ("ns3::UdpSocketFactory",
                            Address (InetSocketAddress (Ipv4Address::GetAny (), port)));
    
    PacketSinkHelper sink4 ("ns3::UdpSocketFactory",
                            Address (InetSocketAddress (Ipv4Address::GetAny (), port)));
    
    PacketSinkHelper sink5 ("ns3::UdpSocketFactory",
                            Address (InetSocketAddress (Ipv4Address::GetAny (), port)));
    
    PacketSinkHelper sink6 ("ns3::UdpSocketFactory",
                            Address (InetSocketAddress (Ipv4Address::GetAny (), port)));

    udpApp1.Add(sink1.Install(cli1));
    udpApp2.Add(sink2.Install(cli2));
    udpApp3.Add(sink3.Install(cli3));
    udpApp4.Add(sink4.Install(cli4));
    udpApp5.Add(sink5.Install(cli5));
    udpApp6.Add(sink6.Install(cli6));

    udpApp1.Start(Seconds(BACKGROUND_START_TIME+1));
    udpApp1.Stop(Seconds(BACKGROUND_END_TIME));
    udpApp2.Start(Seconds(BACKGROUND_START_TIME+1));
    udpApp2.Stop(Seconds(BACKGROUND_END_TIME));
    udpApp3.Start(Seconds(BACKGROUND_START_TIME+1));
    udpApp3.Stop(Seconds(BACKGROUND_END_TIME));
    udpApp4.Start(Seconds(BACKGROUND_START_TIME+1));
    udpApp4.Stop(Seconds(BACKGROUND_END_TIME));
    udpApp5.Start(Seconds(BACKGROUND_START_TIME+1));
    udpApp5.Stop(Seconds(BACKGROUND_END_TIME));
    udpApp6.Start(Seconds(BACKGROUND_START_TIME+1));
    udpApp6.Stop(Seconds(BACKGROUND_END_TIME));

    // Atribui um modelo para gerar erros na transmissão de pacotes dos fluxos UDP.
    // A ideia é apenas simular fluxos "variáveis", de forma aleatória, como uma
    // alternativa a trabalhar VBR no on-off application.
    Ptr<RateErrorModel> em = CreateObject<RateErrorModel>();
    em->SetAttribute("ErrorRate", DoubleValue(0.55));
    em->SetUnit(ns3::RateErrorModel::ErrorUnit(RateErrorModel::ERROR_UNIT_PACKET));
    ndc_r2_srv1.Get(0)->SetAttribute("ReceiveErrorModel", PointerValue(em));
    ndc_r2_srv2.Get(0)->SetAttribute("ReceiveErrorModel", PointerValue(em));
    ndc_r2_srv3.Get(0)->SetAttribute("ReceiveErrorModel", PointerValue(em));
    ndc_r2_srv4.Get(0)->SetAttribute("ReceiveErrorModel", PointerValue(em));
    ndc_r2_srv5.Get(0)->SetAttribute("ReceiveErrorModel", PointerValue(em));
    ndc_r2_srv6.Get(0)->SetAttribute("ReceiveErrorModel", PointerValue(em));

    // Fluxos TCP.

    // Criando sinks...
    // Define porta destino;
    // Pega o IP do sink pra ser usado depois;
    // Cria o socket;
    // Instala o sink no cliente.
    uint16_t sinkPort = 8080;
    uint16_t srcPort = 30000;
    ApplicationContainer sinkApps;

    Address sinkAddress7(InetSocketAddress(ic_r1_cli7.GetAddress(1), sinkPort));
    PacketSinkHelper packetSinkHelper7("ns3::TcpSocketFactory",
                                      InetSocketAddress(Ipv4Address::GetAny(), sinkPort));
    sinkApps = packetSinkHelper7.Install(cli7);
 
    Address sinkAddress8(InetSocketAddress(ic_r1_cli8.GetAddress(1), sinkPort));
    PacketSinkHelper packetSinkHelper8("ns3::TcpSocketFactory",
                                      InetSocketAddress(Ipv4Address::GetAny(), sinkPort));
    sinkApps = packetSinkHelper8.Install(cli8);
 
    Address sinkAddress9(InetSocketAddress(ic_r1_cli9.GetAddress(1), sinkPort));
    PacketSinkHelper packetSinkHelper9("ns3::TcpSocketFactory",
                                      InetSocketAddress(Ipv4Address::GetAny(), sinkPort));
    sinkApps = packetSinkHelper9.Install(cli9);
 
    Address sinkAddress10(InetSocketAddress(ic_r1_cli10.GetAddress(1), sinkPort));
    PacketSinkHelper packetSinkHelper10("ns3::TcpSocketFactory",
                                      InetSocketAddress(Ipv4Address::GetAny(), sinkPort));
    sinkApps = packetSinkHelper10.Install(cli10);
 
    sinkApps.Start(Seconds(BACKGROUND_START_TIME));
    sinkApps.Stop(Seconds(BACKGROUND_END_TIME));

    // Criando servidores...
    // Cria o socket com algoritmo específico de CW;
    // Configura a conexão;
    // Adiciona/instala a aplicação.

    // Fluxo aproximando Netflix. Pacote de tamanho 1492 (1438 payload + 54 overhead)
    // A Netflix usa o próprio algoritmo TCP, fechado, então escolhi outro.
    std::stringstream nodeId7;
    nodeId7 << srv7->GetId();
    std::string specificNode7 = "/NodeList/" + nodeId7.str() + "/$ns3::TcpL4Protocol/SocketType";
    Config::Set(specificNode7, TypeIdValue(TypeId::LookupByName("ns3::TcpNewReno")));
    Ptr<Socket> ns3TcpSocket7 = Socket::CreateSocket(srv7, TcpSocketFactory::GetTypeId());
    Ptr<TutorialApp> app7 = CreateObject<TutorialApp>();
    app7->Setup(ns3TcpSocket7, sinkAddress7, 1438, 10000000, DataRate("1Mbps"));
    srv7->AddApplication(app7);
    app7->SetStartTime(Seconds(BACKGROUND_START_TIME+5));
    app7->SetStopTime(Seconds(BACKGROUND_END_TIME));

    // Fluxo aproximando Prime e Globo. Pacote de tamanho 1480 (1426 payload + 54 overhead)
    // Também não se sabe o tipo de algoritmo usado. Escolhi um que convém.
    std::stringstream nodeId8;
    nodeId8 << srv8->GetId();
    std::string specificNode8 = "/NodeList/" + nodeId8.str() + "/$ns3::TcpL4Protocol/SocketType";
    Config::Set(specificNode8, TypeIdValue(TypeId::LookupByName("ns3::TcpCubic")));
    Ptr<Socket> ns3TcpSocket8 = Socket::CreateSocket(srv8, TcpSocketFactory::GetTypeId());
    Ptr<TutorialApp> app8 = CreateObject<TutorialApp>();
    app8->Setup(ns3TcpSocket8, sinkAddress8, 1426, 10000000, DataRate("1Mbps"));
    srv8->AddApplication(app8);
    app8->SetStartTime(Seconds(BACKGROUND_START_TIME+5));
    app8->SetStopTime(Seconds(BACKGROUND_END_TIME));

    // Fluxo genérico só pra completar tabela.
    // Tamanho intermediário 566 (512 payload + 54 overhead)
    std::stringstream nodeId9;
    nodeId9 << srv9->GetId();
    std::string specificNode9 = "/NodeList/" + nodeId9.str() + "/$ns3::TcpL4Protocol/SocketType";
    Config::Set(specificNode9, TypeIdValue(TypeId::LookupByName("ns3::TcpCubic")));
    Ptr<Socket> ns3TcpSocket9 = Socket::CreateSocket(srv9, TcpSocketFactory::GetTypeId());
    Ptr<TutorialApp> app9 = CreateObject<TutorialApp>();
    app9->Setup(ns3TcpSocket9, sinkAddress9, 512, 10000000, DataRate("1Mbps"));
    srv9->AddApplication(app9);
    app9->SetStartTime(Seconds(BACKGROUND_START_TIME+5));
    app9->SetStopTime(Seconds(BACKGROUND_END_TIME));

    // Fluxo do experimento. Pacote de tamanho entre intermediário e máximo.
    // Tamanho 1300 (1246 payload + 54 overhead)
    std::stringstream nodeId10;
    nodeId10 << srv10->GetId();
    std::string specificNode10 = "/NodeList/" + nodeId10.str() + "/$ns3::TcpL4Protocol/SocketType";
    Config::Set(specificNode10, TypeIdValue(TypeId::LookupByName("ns3::TcpWestwood")));
    Ptr<Socket> ns3TcpSocket10 = Socket::CreateSocket(srv10, TcpSocketFactory::GetTypeId());
    Ptr<TutorialApp> app10 = CreateObject<TutorialApp>();
    app10->Setup(ns3TcpSocket10, sinkAddress10, 1246, 10000000, DataRate("1Mbps"));
    srv10->AddApplication(app10);
    app10->SetStartTime(Seconds(BACKGROUND_START_TIME+30));
    app10->SetStopTime(Seconds(BACKGROUND_END_TIME));

    // Trace do congestion window dos fluxos TCP
    AsciiTraceHelper asciiTraceHelper;
    Ptr<OutputStreamWrapper> stream7 = asciiTraceHelper.CreateFileStream("fluxo07.cwnd");
    Ptr<OutputStreamWrapper> stream8 = asciiTraceHelper.CreateFileStream("fluxo08.cwnd");
    Ptr<OutputStreamWrapper> stream9 = asciiTraceHelper.CreateFileStream("fluxo09.cwnd");
    Ptr<OutputStreamWrapper> stream10 = asciiTraceHelper.CreateFileStream("fluxo10.cwnd");
    ns3TcpSocket7->TraceConnectWithoutContext("CongestionWindow",
                                             MakeBoundCallback(&CwndChange, stream7));
    ns3TcpSocket8->TraceConnectWithoutContext("CongestionWindow",
                                             MakeBoundCallback(&CwndChange, stream8));
    ns3TcpSocket9->TraceConnectWithoutContext("CongestionWindow",
                                             MakeBoundCallback(&CwndChange, stream9));
    ns3TcpSocket10->TraceConnectWithoutContext("CongestionWindow",
                                             MakeBoundCallback(&CwndChange, stream10));

    // Trace dos pacotes dos fluxos TCP
    Ptr<OutputStreamWrapper> stream_srv7 = asciiTraceHelper.CreateFileStream("srv07.txt");
    ndc_r2_srv7.Get(1)->TraceConnectWithoutContext("PhyTxEnd", MakeBoundCallback(&TxPacketDone, stream_srv7));

    // Trace dos pacotes sendo recebidos pelos clientes
    Ptr<OutputStreamWrapper> stream_cli7 = asciiTraceHelper.CreateFileStream("cli70.txt");
    ndc_r1_cli7.Get(1)->TraceConnectWithoutContext("PhyRxEnd", MakeBoundCallback(&RxPacketDone, stream_cli7));

    // Trace dos pacotes sendo enviados pelos servidores
    Ptr<OutputStreamWrapper> stream_srv8 = asciiTraceHelper.CreateFileStream("srv8.txt");
    ndc_r2_srv8.Get(1)->TraceConnectWithoutContext("PhyTxEnd", MakeBoundCallback(&TxPacketDone, stream_srv8));

    // Trace dos pacotes sendo recebidos pelos clientes
    Ptr<OutputStreamWrapper> stream_cli8 = asciiTraceHelper.CreateFileStream("cli8.txt");
    ndc_r1_cli8.Get(1)->TraceConnectWithoutContext("PhyRxEnd", MakeBoundCallback(&RxPacketDone, stream_cli8));

    // Trace dos pacotes sendo enviados pelos servidores
    Ptr<OutputStreamWrapper> stream_srv9 = asciiTraceHelper.CreateFileStream("srv9.txt");
    ndc_r2_srv9.Get(1)->TraceConnectWithoutContext("PhyTxEnd", MakeBoundCallback(&TxPacketDone, stream_srv9));

    // Trace dos pacotes sendo recebidos pelos clientes
    Ptr<OutputStreamWrapper> stream_cli9 = asciiTraceHelper.CreateFileStream("cli9.txt");
    ndc_r1_cli9.Get(1)->TraceConnectWithoutContext("PhyRxEnd", MakeBoundCallback(&RxPacketDone, stream_cli9));

    // Trace dos pacotes sendo enviados pelos servidores
    Ptr<OutputStreamWrapper> stream_srv10 = asciiTraceHelper.CreateFileStream("srv10.txt");
    ndc_r2_srv10.Get(1)->TraceConnectWithoutContext("PhyTxEnd", MakeBoundCallback(&TxPacketDone, stream_srv10));

    // Trace dos pacotes sendo recebidos pelos clientes
    Ptr<OutputStreamWrapper> stream_cli10 = asciiTraceHelper.CreateFileStream("cli10.txt");
    ndc_r1_cli10.Get(1)->TraceConnectWithoutContext("PhyRxEnd", MakeBoundCallback(&RxPacketDone, stream_cli10));

    // Cria pcap das interfaces de clientes e servidores
    p2p.EnablePcap("srv1.pcap", ndc_r2_srv1.Get(1));
    p2p.EnablePcap("srv2.pcap", ndc_r2_srv2.Get(1));
    p2p.EnablePcap("srv3.pcap", ndc_r2_srv3.Get(1));
    p2p.EnablePcap("srv4.pcap", ndc_r2_srv4.Get(1));
    p2p.EnablePcap("srv5.pcap", ndc_r2_srv5.Get(1));
    p2p.EnablePcap("srv6.pcap", ndc_r2_srv6.Get(1));
    p2p.EnablePcap("srv7.pcap", ndc_r2_srv7.Get(1));
    p2p.EnablePcap("srv8.pcap", ndc_r2_srv8.Get(1));
    p2p.EnablePcap("srv9.pcap", ndc_r2_srv9.Get(1));
    p2p.EnablePcap("srv10.pcap", ndc_r2_srv10.Get(1));
    p2p.EnablePcap("cli1.pcap", ndc_r1_cli1.Get(1));
    p2p.EnablePcap("cli2.pcap", ndc_r1_cli2.Get(1));
    p2p.EnablePcap("cli3.pcap", ndc_r1_cli3.Get(1));
    p2p.EnablePcap("cli4.pcap", ndc_r1_cli4.Get(1));
    p2p.EnablePcap("cli5.pcap", ndc_r1_cli5.Get(1));
    p2p.EnablePcap("cli6.pcap", ndc_r1_cli6.Get(1));
    p2p.EnablePcap("cli7.pcap", ndc_r1_cli7.Get(1));
    p2p.EnablePcap("cli8.pcap", ndc_r1_cli8.Get(1));
    p2p.EnablePcap("cli9.pcap", ndc_r1_cli9.Get(1));
    p2p.EnablePcap("cli10.pcap", ndc_r1_cli10.Get(1));

    Simulator::Stop(Seconds(310));
    Simulator::Run();
    Simulator::Destroy();

    return 0;
}

