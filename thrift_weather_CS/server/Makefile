
target = server
gencpp = ../gen-cpp/
CPPFLAGS = -g -I$(gencpp) -I ~/domob/LIB/domob-lib/output/include/ -L ~/domob/LIB/domob-lib/output/lib/
objects = $(gencpp)weatherCS_constants.o $(gencpp)weather.o weather_server.o $(gencpp)weatherCS_types.o main.o
server : $(objects)
	g++ $(CPPFLAGS) -o $(target) -lthrift -lboost_thread $(objects) -llog4cpp  -ldomoblib
	
# pull in dependency info for *existing* .o files
-include $(objects:.o=.d)

# compile and generate dependency info;
# more complicated dependency computation, so all prereqs listed
# will also become command-less, prereq-less targets
#   sed:    strip the target (everything before colon)
#   sed:    remove any continuation backslashes
#   fmt -1: list words one per line
#   sed:    strip leading spaces
#   sed:    add trailing colons
$(objects) : %.o : %.cpp
	g++ -c $(CPPFLAGS) $< -o $@
	@g++ -MM $(CPPFLAGS) $< > $(@:.o=.d)
	@mv -f $(@:.o=.d) $(@:.o=.d).tmp
	@sed -e 's|.*:|$*.o:|' < $(@:.o=.d).tmp > $(@:.o=.d)
	@sed -e 's/.*://' -e 's/\\$$//' < $(@:.o=.d).tmp | fmt -1 | \
		sed -e 's/^ *//' -e 's/$$/:/' >> $(@:.o=.d)
	@rm -f $(@:.o=.d).tmp

.PHONY : clean
clean :
	-rm $(objects) $(target) $(objects:.o=.d)
