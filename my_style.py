color_scale = [
    '#636EFA', '#00CC96', '#AB63FA', '#FFA15A', '#EF553B', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52',
    '#1F77B4', '#FF7F0E', '#2CA02C', '#D62728', '#9467BD', '#8C564B', '#E377C2', '#7F7F7F', '#BCBD22', '#17BECF',
    '#3366CC', '#DC3912', '#FF9900', '#109618', '#990099', '#0099C6', '#DD4477', '#66AA00', '#B82E2E', '#316395',
    '#4C78A8', '#F58518', '#E45756', '#72B7B2', '#54A24B', '#EECA3B', '#B279A2', '#FF9DA6', '#9D755D', '#BAB0AC'
]

def generate_stylesheet():
    my_stylesheet = [
        {
        "selector": "core",
        "style": {
            "selection-box-color": "#AAD8FF",
            "selection-box-border-color": "#8BB0D0",
            "selection-box-opacity": "0.5"
        }},
        {
        "selector": "node",
        "style": {
            "width": "mapData(score, 0, 0.006769776522008331, 20, 60)",
            "height": "mapData(score, 0, 0.006769776522008331, 20, 60)",
            "content": "data(id)",
            "font-size": "20px",
            "text-valign": 'bottom',
            # "text-valign": "surper",
            "text-halign": "center",
            "background-color": "#dbe8ff",
            "text-outline-color": "#2e2e2e",
            "text-outline-width": "1px",
            "color": "#2e2e2e",
            "overlay-padding": "6px",
            "z-index": "10"
        }
        }, 
        {
        "selector": "node:selected",
        "style": {
            "border-width": "8px",
            "border-color": "#CB4B16",
            "border-opacity": "0.5",
            "background-color": "#CB4B16",
            "text-outline-color": "#CB4B16",
            "color": "#f06d37"
            }
        },{
        "selector": "edge:selected",
        "style": {
            "line-color": "#f26e5a",
        }
        },{
        "selector": ".missing",
        "style": {
            # "shape": 'square',
            "background-color": "#404040",
        }
        },{
        "selector": ".causality",
        "style": {
            "shape": 'square',
            # "background-color": "#f553ba",
            "background-color": "#fcba03",
        } 
        },{
        "selector": ".responsive",
        "style": {
            "shape": 'square',
            # "background-color": "#fcba03",
            "background-color": "#80ff99",
        }
        },{
        "selector": ".havedrug",
        "style": {
            "background-color": "#f54242",
        } 
        },{
        "selector": ".kamei",
        "style": {
            "width": "60",
            "height": "60",
        } 
        },
        # {
        # "selector": "edge",
        # "style": {
        #     "curve-style": "bezier",
        #     "haystack-radius": "0.7",
        #     "opacity": "1",
        #     "line-color": "#bbb",
        #     "width": "mapData(weight, 0, 1, 1, 500)",
        #     "overlay-padding": "3px",
        # }}
    ]

    # for num in range(max_id):
    #     color = color_scale[num%10]
    #     style = {
    #         "selector": "edge[networkgroupId={}]".format(num) ,
    #         "style": { 
    #             "line-color": color,
    #             'target-arrow-color': color,
    #             'target-arrow-shape': 'vee',
    #         }
    #     }

    #     my_stylesheet.append(style)
    
    return my_stylesheet