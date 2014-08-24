gen_dep = gen-cpp/weather_server.skeleton.cpp

.PHONY : server
server : $(gen_dep)
	@make -C server

$(gen_dep) : weatherCS.thrift
	thrift --gen cpp --gen py:utf8strings weatherCS.thrift

.PHONY : clean
clean :
	@make -C server clean
	-rm -rf gen-cpp/ gen-py/
