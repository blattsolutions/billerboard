var simplemaps_countrymap_mapdata = {
  main_settings: {
    //General settings
    // width: "600", //'700' or 'responsive'
    width: "900",
    background_color: "#FFFFFF",
    background_transparent: "yes",
    border_color: "#ffffff",

    //State defaults
    state_color: "#88A4BC",
    state_hover_color: "#3B729F",
    state_url: "",
    border_size: 1.5,
    all_states_inactive: "no",
    all_states_zoomable: "yes",

    //Location defaults
    location_description: "Location description",
    location_url: "",
    location_color: "#FF0067",
    location_opacity: 0.8,
    location_hover_opacity: 1,
    location_size: 25,
    location_type: "square",
    location_image_source: "frog.png",
    location_border_color: "#FFFFFF",
    location_border: 2,
    location_hover_border: 2.5,
    all_locations_inactive: "no",
    all_locations_hidden: "no",

    //Label defaults
    label_color: "#ffffff",
    label_hover_color: "#ffffff",
    label_size: 16,
    label_font: "Arial",
    label_display: "auto",
    label_scale: "yes",
    hide_labels: "no",
    hide_eastern_labels: "no",

    //Zoom settings
    zoom: "yes",
    manual_zoom: "yes",
    back_image: "no",
    initial_back: "no",
    initial_zoom: "-1",
    initial_zoom_solo: "no",
    region_opacity: 1,
    region_hover_opacity: 0.6,
    zoom_out_incrementally: "yes",
    zoom_percentage: 0.99,
    zoom_time: 0.5,

    //Popup settings
    popup_color: "white",
    popup_opacity: 0.9,
    popup_shadow: 1,
    popup_corners: 5,
    popup_font: "12px/1.5 Verdana, Arial, Helvetica, sans-serif",
    popup_nocss: "no",

    //Advanced settings
    div: "map",
    auto_load: "yes",
    url_new_tab: "no",
    images_directory: "default",
    fade_time: 0.1,
    link_text: "View Website",
    popups: "detect",
    state_image_url: "",
    state_image_position: "",
    location_image_url: "",
  },
  state_specific: {
    DEBB: {
      name: "Brandenburg",
      description: "No one here",
    },
    DEBE: {
      name: "Berlin",
      description: "No one here",

    },
    DEBW: {
      name: "Baden-Württemberg",
      description: "No one here",

    },
    DEBY: {
      name: "Bayern",
      description: "No one here",

    },
    DEHB: {
      name: "Bremen",
      description: "No one here",

    },
    DEHE: {
      name: "Hessen",
      description: "No one here",

    },
    DEHH: {
      name: "Hamburg",
      description: "No one here",

    },
    DEMV: {
      name: "Mecklenburg-Vorpommern",
      description: "No one here",

    },
    DENI: {
      name: "Niedersachsen",
      description: "No one here",

    },
    DENW: {
      name: "Nordrhein-Westfalen",
      description: "No one here",

    },
    DERP: {
      name: "Rheinland-Pfalz",
      description: "No one here",

    },
    DESH: {
      name: "Schleswig-Holstein",
      description: "No one here",

    },
    DESL: {
      name: "Saarland",
      description: "No one here",

    },
    DESN: {
      name: "Sachsen",
      description: "No one here",

    },
    DEST: {
      name: "Sachsen-Anhalt",
      description: "No one here",

    },
    DETH: {
      name: "Thüringen",
      description: "No one here",

    },
  },
  locations: {},
  labels: {
    DEBB: {
      name: "Brandenburg",
      parent_id: "DEBB",
    },
    DEBE: {
      name: "Berlin",
      parent_id: "DEBE",
    },
    DEBW: {
      name: "Baden-Württemberg",
      parent_id: "DEBW",
    },
    DEBY: {
      name: "Bayern",
      parent_id: "DEBY",
    },
    DEHB: {
      name: "Bremen",
      parent_id: "DEHB",
    },
    DEHE: {
      name: "Hessen",
      parent_id: "DEHE",
    },
    DEHH: {
      name: "Hamburg",
      parent_id: "DEHH",
    },
    DEMV: {
      name: "Mecklenburg-Vorpommern",
      parent_id: "DEMV",
    },
    DENI: {
      name: "Niedersachsen",
      parent_id: "DENI",
    },
    DENW: {
      name: "Nordrhein-Westfalen",
      parent_id: "DENW",
    },
    DERP: {
      name: "Rheinland-Pfalz",
      parent_id: "DERP",
    },
    DESH: {
      name: "Schleswig-Holstein",
      parent_id: "DESH",
    },
    DESL: {
      name: "Saarland",
      parent_id: "DESL",
    },
    DESN: {
      name: "Sachsen",
      parent_id: "DESN",
    },
    DEST: {
      name: "Sachsen-Anhalt",
      parent_id: "DEST",
    },
    DETH: {
      name: "Thüringen",
      parent_id: "DETH",
    },
  },
  legend: {
    entries: [],
  },
  regions: {},
};

let listArray = [];
async function updateMapData() {
  try {
    const response = await fetch('http://127.0.0.1:8000/staff-list-api/');
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json();
    const groupedByStateCode = data.reduce((acc, item) => {
      if (!acc[item.state_code]) {
        acc[item.state_code] = {
          id: item.id,
          state_code: item.state_code,
          state_name: item.state_name,
          staffName: []
        };
      }
      acc[item.state_code].staffName.push({
        staffId: item.id,
        username: item.username,
        email: item.email
      });
      return acc;
    }, {});

    const result = Object.values(groupedByStateCode);
    listArray = result;

    result.forEach((staff) => {
      const code = staff.state_code;
      const stateName = staff.state_name;
      const desStaffName = staff.staffName
        .map((s) => ` - ${s.username} (${s.email})<br />`)
        .join("");
      if (simplemaps_countrymap_mapdata.state_specific[code]) {
        simplemaps_countrymap_mapdata.labels[code].name = stateName;
        simplemaps_countrymap_mapdata.state_specific[code].description = desStaffName || "No one here";
      }
    });

    const mapContainer = document.getElementById('map');
    mapContainer.innerHTML = '';

    simplemaps_countrymap.load();
    return listArray;
  } catch (error) {
    console.error('Error:', error);
    return [];
  }
}
updateMapData().then(() => {
  console.log("listArray", listArray);
});
