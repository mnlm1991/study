
.PHONY : server
server : 
	@make -C gen-cpp

.PHONY : gen
gen : weatherCS.thrift
	thrift --gen cpp --gen py weatherCS.thrift
