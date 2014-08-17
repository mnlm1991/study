
objects = weather_constants.o weather.o weather_server.o weather_types.o
server : $(objects)
	g++ -o server -lthrift -lboost_thread-mt $(objects)
	
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
%.o : %.cpp
	g++ -c $(CPPFLAGS) $*.cpp -o $*.o
	@g++ -MM $(CPPFLAGS) $*.cpp > $*.d
	@mv -f $*.d $*.d.tmp
	@sed -e 's|.*:|$*.o:|' < $*.d.tmp > $*.d
	@sed -e 's/.*://' -e 's/\\$$//' < $*.d.tmp | fmt -1 | \
	  sed -e 's/^ *//' -e 's/$$/:/' >> $*.d
	@rm -f $*.d.tmp

.PHONY : clean
clean :
	-rm $(objects) server *.d
