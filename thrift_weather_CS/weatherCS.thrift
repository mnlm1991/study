
struct weather_info{
1: string city_id,
2: string name,
3: i32    max_temp,
4: i32    min_temp,
}

enum SortMethod{
	Up,
	Down
}
service weather{
	/** get the weather info after sorted by max_temp*/
	list<weather_info> get_weather_info_sorted_list(1: SortMethod method),

	/** get the weaether info by city_id */
	weather_info get_weather_info(1: string city_id)
}
