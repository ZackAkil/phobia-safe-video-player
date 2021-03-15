
def get_time(time_json):
    output = 0
    output += time_json.get('seconds', 0)
    output += time_json.get('nanos', 0) * 1e-9
    return output


def merge_overlaping_segments(sorted_segments):

    merged_segments = []

    for seg in sorted_segments:

        # if its empty add the first one     
        if not merged_segments:
            merged_segments.append(seg)
            continue
        
        # if the start of the next segment is within the previous segment
        # then just extend the previous segment         
        if seg[0] <= merged_segments[-1][1]:
            merged_segments[-1][1] = seg[1]
        else:
            merged_segments.append(seg)

    return merged_segments
    

def get_segments_for_labels(labels, annotations):
    '''
    Find all the segments within the annotations that match any of the labels
    '''
    
    segments = []
    
    for s in annotations:
        
        label_match = False

#         print(s['entity']['description'])
        
        # if the lebel we are looking for matches the entity or the category         
        if s['entity']['description'] in labels:
            label_match = True
        elif 'category_entities' in s:
            if s['category_entities'][0]['description'] in labels:
                label_match = True

        if label_match:
            for seg in s['segments']:
                start_time = get_time( seg['segment']['start_time_offset'])
                end_time = get_time( seg['segment']['end_time_offset'])
                segments.append( [start_time, end_time] )
#                 print('from {} -> {}'.format(start_time, end_time))

    sorted_segments = sorted(segments)
    merged_segments = merge_overlaping_segments(sorted_segments)

    return merged_segments
