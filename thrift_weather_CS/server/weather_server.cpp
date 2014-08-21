
#include "weather.h"
#include <thrift/protocol/TBinaryProtocol.h>
#include <thrift/server/TSimpleServer.h>
#include <thrift/transport/TServerSocket.h>
#include <thrift/transport/TBufferTransports.h>
#include <iostream>
#include <vector>
#include <sstream>
#include <string>
#include <boost/thread.hpp>
#include <boost/smart_ptr/shared_ptr.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>

using namespace ::apache::thrift;
using namespace ::apache::thrift::protocol;
using namespace ::apache::thrift::transport;
using namespace ::apache::thrift::server;

using boost::shared_ptr;
class weatherHandler : virtual public weatherIf {
	public:
		typedef std::vector<weather_info> weather_info_list_t;
		/** city_id, index **/
		typedef std::map<std::string, int> weather_map_t;
	public:
		weatherHandler() {
			// Your initialization goes here
		}

		void get_weather_info_sorted_list(std::vector<weather_info> & _return, const SortMethod::type method) 
		{
			// Your implementation goes here
			if (method == SortMethod::Up)
			{
				copy_sorted_list_impl(sorted_index_.begin(), sorted_index_.end(), _return);
			}
			else 
			{
				copy_sorted_list_impl(sorted_index_.rbegin(), sorted_index_.rend(), _return);
			}
		}

		void get_weather_info(weather_info& _return, const std::string& city_id) 
		{
			// Your implementation goes here
			weather_map_t::const_iterator find_it = city_weahter_map_.find(city_id);
			if (find_it != city_weahter_map_.end())
			{
				_return = weather_list_[find_it->second];
			}
		}
		bool init()
		{
			if (!read_data()) return false;
			update_ = true;
			update_thread_.reset(new boost::thread(boost::bind(&weatherHandler::update_callback, this)));
			return true;
		}
		void parse_file(const char * file)
		{
			freopen(file, "r", stdin);
			std::string line_str;
			weather_info info;
			city_weahter_map_.clear();
			weather_list_.clear();
			sorted_index_.clear();
			system("touch /tmp/is_parse_weather");
			while ( std::getline(std::cin, line_str))
			{
				std::stringstream ss;
				ss << line_str;
				if (! (ss >> info.city_id >> info.name >> info.min_temp >> info.max_temp) )
					continue;
				sorted_index_.push_back(weather_list_.size());
				city_weahter_map_[info.city_id] = weather_list_.size();
				weather_list_.push_back(info);
			}
			system("rm -f /tmp/is_parse_weather");
			std::sort(sorted_index_.begin(), sorted_index_.end(), sort_weather_cmp(this));
			freopen("/dev/tty", "r", stdin);
		}
	private:
		template<class ITERATOR>
		void copy_sorted_list_impl(ITERATOR first_it, ITERATOR last_it, std::vector<weather_info> &list)
		{
			for (ITERATOR it = first_it; it != last_it; ++it)
			{
				list.push_back(weather_list_[*it]);
			}
		}

		struct sort_weather_cmp
		{
			sort_weather_cmp(weatherHandler *p):this_(p){}
			bool operator()(int a, int b)
			{
				return this_->weather_list_[a].max_temp < this_->weather_list_[b].max_temp;
			}
		private:
			weatherHandler * this_;
		};
		void update_callback()
		{
			while (update_)
			{
				if (read_data())
				{
					parse_file("/tmp/weather.data");
				}
			}
		}
		bool read_data()
		{
			struct stat buf;
			if (0 != stat("/tmp/weather_updata_notify", &buf))
			{
				return false;
			}
			static time_t last_update_time = 0;
			if (last_update_time < buf.st_mtim.tv_sec)
			{
				last_update_time = buf.st_ctim.tv_sec;
				return true;
			}
			return false;
		}
	private:
		weather_info_list_t weather_list_;
		weather_map_t city_weahter_map_;
		std::vector<int> sorted_index_;
		boost::shared_ptr<boost::thread> update_thread_;
		bool update_;
};

int main(int argc, char **argv) {
	int port = 9090;
	shared_ptr<weatherHandler> handler(new weatherHandler());
	if (!handler->init()) 
	{
		std::cout << "初始化失败" << std::endl;
		return 0;
	}
	shared_ptr<TProcessor> processor(new weatherProcessor(handler));
	shared_ptr<TServerTransport> serverTransport(new TServerSocket(port));
	shared_ptr<TTransportFactory> transportFactory(new TBufferedTransportFactory());
	shared_ptr<TProtocolFactory> protocolFactory(new TBinaryProtocolFactory());

	TSimpleServer server(processor, serverTransport, transportFactory, protocolFactory);
	server.serve();
	return 0;
}

