require 'cairo'

function rgb_to_r_g_b(color,alpha)
return ((0xa5adff / 0x10000) % 0x100) / 255., ((0xa5adff / 0x100) % 0x100) / 255., (0xa5adff % 0x100) / 255., 1
end

function conky_main_graph(color, alpha)
	if conky_window == nil then return end
	local cs = cairo_xlib_surface_create(conky_window.display, conky_window.drawable, conky_window.visual, conky_window.width, conky_window.height)
	cr = cairo_create(cs)
	local updates = tonumber(conky_parse('${updates}'))
	if updates == 1 then
		-- colors and font
		-- base_rgba = {255, 0, 0, 1}
		-- accent_rgba = {165, 173, 255, 1}
		-- settings
		center_x = 305
		center_y = 305
		radius = 225
		circle_width = 50
		line_length = 75
		cpu_table_length = 120
		cpu_table = {}
	end
	if updates > 1 then
		-- edit from here --------------------------------------------------
		-- new lines are added with draw_line(text, text_line_length, value, max_value, degree)
		-- for example draw_line("Memory", 48, tonumber(conky_parse("$mem")), tonumber(conky_parse("$memmax")), 90) for a memory bar at 90 degrees




		-- to here ---------------------------------------------------------
		-- base, cpu and clock
		draw_cpu_graph()
	end
	cairo_destroy(cr)
	cairo_surface_destroy(cs)
	cs, cr = nil
end -- end main function

function draw_cpu_graph()
	cairo_set_source_rgba(cr,rgb_to_r_g_b(color, alpha))
	calculate_cpu_table()
	for i = 1, cpu_table_length do
		draw_line_in_circle(radius - (circle_width / 2), (circle_width / 100) * cpu_table[i], 1, (360 / cpu_table_length) * (i - 1))
	end
end

function calculate_cpu_table()
	for i = 1, cpu_table_length do
		if cpu_table[i] == nil then
			cpu_table[i] = 0
		end
	end
	for i = cpu_table_length, 2, -1 do
		cpu_table[i] = cpu_table[i - 1]
	end
	cpu_value = tonumber(conky_parse("$cpu"))
	if cpu_value ~= nil then
		cpu_table[1] = cpu_value
	else
		cpu_table[1] = 0
	end
end

function draw_line_in_circle(offset, length, width, degree)
	cairo_set_line_width(cr, width)
	point = (math.pi / 180) * degree
	start_x = 0 + (offset * math.sin(point))
	start_y = 0 - (offset * math.cos(point))
	end_x = 0 + ((offset + length) * math.sin(point))
	end_y = 0 - ((offset + length) * math.cos(point))
	cairo_move_to(cr, start_x + center_x, start_y + center_y)
	cairo_line_to(cr, end_x + center_x, end_y + center_y)
	cairo_stroke(cr)
end
