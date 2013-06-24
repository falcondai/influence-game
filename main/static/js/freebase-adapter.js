// convert freebase response json into canonical data object
function prepare_freebase_data(json) {
	// prepare data for representation
	var data = {'nodes': [], 'links': []};
	
	// 0th node is the focal node
	data.nodes.push({
		'name': json.result.name,
		'start': (json.result['/music/artist/active_start'])? parseInt(json.result['/music/artist/active_start'].substring(0,4)) : null,
		'end': (json.result['/music/artist/active_end'])? parseInt(json.result['/music/artist/active_end'].substring(0, 4)) : null,
	});
	var last = 0;
	
	// push in the influenced
	for (var n in json.result.influenced) {
		var node = json.result.influenced[n];
		data.nodes.push({
			'name': node.name,
			'start': (node['/music/artist/active_start'])? parseInt(node['/music/artist/active_start'].substring(0,4)) : null,
			'end': (node['/music/artist/active_end'])? parseInt(node['/music/artist/active_end'].substring(0,4)) : null,
		});
		last ++;
		data.links.push({
			'influence': 0,
			'source': 0,
			'target': last,
		});
	}
	
	// push in the influenced_by
	for (var n in json.result.influenced_by) {
		var node = json.result.influenced_by[n];
		data.nodes.push({
			'name': node.name,
			'start': (node['/music/artist/active_start'])? parseInt(node['/music/artist/active_start'].substring(0,4)) : null,
			'end': (node['/music/artist/active_end'])? parseInt(node['/music/artist/active_end'].substring(0,4)) : null,
		});
		last ++;
		data.links.push({
			'influence': 0,
			'source': last,
			'target': 0,
		});
	}
	
	return data;
}