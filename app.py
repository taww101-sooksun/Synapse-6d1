import math
import io
import json
from pathlib import Path
from datetime import datetime

import folium
import streamlit as st
from folium.plugins import LocateControl, Draw
from branca.element import MacroElement
from streamlit_folium import st_folium
from streamlit_geolocation import streamlit_geolocation
import requests
from PIL import Image, ImageDraw

st.set_page_config(
    page_title="Ta App - เธงเธฑเธ”เธเธทเนเธเธ—เธตเนเธเธฒ",
    page_icon="๐พ",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
html, body, [class*="css"], .stApp, button, input, textarea, select {
    font-family: Tahoma, Arial, sans-serif !important;
}
.total-box {
    padding: 24px;
    border-radius: 18px;
    background: rgba(46,125,50,.12);
    border: 2px solid rgba(46,125,50,.35);
    text-align: center;
    margin-top: 10px;
}
.total-money { font-size: 42px; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

PLOW_RATE = 250.0
MILL_RATE = 350.0
RAI_M2 = 1600.0
NGAN_M2 = 400.0
WA_M2 = 4.0

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "ta_data.json"

def load_saved():
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []

def save_saved(data):
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

def thai_area(m2):
    m2 = max(float(m2), 0.0)
    rai = int(m2 // RAI_M2)
    remain = m2 - rai * RAI_M2
    ngan = int(remain // NGAN_M2)
    remain -= ngan * NGAN_M2
    wa = int(remain // WA_M2)
    remain -= wa * WA_M2
    return rai, ngan, wa, remain

def polygon_area_m2(points):
    if len(points) < 3:
        return 0.0
    lat0 = math.radians(sum(p[0] for p in points) / len(points))
    radius = 6378137.0
    xy = []
    for lat, lon in points:
        x = math.radians(lon) * radius * math.cos(lat0)
        y = math.radians(lat) * radius
        xy.append((x, y))
    area = 0.0
    for i in range(len(xy)):
        x1, y1 = xy[i]
        x2, y2 = xy[(i + 1) % len(xy)]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0

def money(value):
    return f"{value:,.2f}"

def get_polygon(drawings):
    if not drawings:
        return []
    for feature in reversed(drawings):
        geometry = feature.get("geometry", {})
        if geometry.get("type") != "Polygon":
            continue
        rings = geometry.get("coordinates", [])
        if not rings:
            continue
        ring = rings[0]
        points = [(float(p[1]), float(p[0])) for p in ring if len(p) >= 2]
        if len(points) > 1 and points[0] == points[-1]:
            points.pop()
        if len(points) >= 3:
            return points
    return []

def make_snapshot(points):
    if len(points) < 3:
        return None
    lats = [p[0] for p in points]
    lons = [p[1] for p in points]
    lat_pad = max((max(lats) - min(lats)) * 0.20, 0.0003)
    lon_pad = max((max(lons) - min(lons)) * 0.20, 0.0003)
    south = min(lats) - lat_pad
    north = max(lats) + lat_pad
    west = min(lons) - lon_pad
    east = max(lons) + lon_pad

    url = (
        "https://server.arcgisonline.com/ArcGIS/rest/services/"
        "World_Imagery/MapServer/export"
    )
    params = {
        "bbox": f"{west},{south},{east},{north}",
        "bboxSR": "4326",
        "imageSR": "4326",
        "size": "1000,700",
        "format": "png",
        "f": "image",
    }
    try:
        response = requests.get(url, params=params, timeout=20)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content)).convert("RGB")
        draw = ImageDraw.Draw(image)
        width, height = image.size
        pixel_points = []
        for lat, lon in points:
            x = (lon - west) / (east - west) * (width - 1)
            y = (north - lat) / (north - south) * (height - 1)
            pixel_points.append((int(x), int(y)))
        draw.line(
            pixel_points + [pixel_points[0]],
            fill=(0, 190, 80),
            width=7,
        )
        return image
    except Exception:
        return None

def image_to_base64(image):
    if image is None:
        return None
    import base64
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")

def base64_to_image(value):
    if not value:
        return None
    import base64
    try:
        return Image.open(io.BytesIO(base64.b64decode(value)))
    except Exception:
        return None

if "points" not in st.session_state:
    st.session_state.points = []
if "saved_plots" not in st.session_state:
    st.session_state.saved_plots = load_saved()
if "lat" not in st.session_state:
    st.session_state.lat = None
if "lon" not in st.session_state:
    st.session_state.lon = None

st.title("๐พ Ta App")
st.caption("เธงเธฑเธ”เธเธทเนเธเธ—เธตเนเธเธฒ โ€ข เธเธฃเธฑเธเนเธเธงเน€เธเธ• โ€ข เธเธณเธเธงเธ“เธเนเธฒเนเธ–/เธเธฑเนเธเธ”เธดเธ โ€ข เธเธฑเธเธ—เธถเธเธเธฃเนเธญเธกเธ เธฒเธ")

# เธเธญ GPS เธเธญเธเน€เธเธฃเธทเนเธญเธเธ—เธตเนเน€เธเธดเธ”เนเธญเธ
location = streamlit_geolocation()

if isinstance(location, dict):
    gps_lat = location.get("latitude")
    gps_lon = location.get("longitude")
    if gps_lat is not None and gps_lon is not None:
        new_lat = float(gps_lat)
        new_lon = float(gps_lon)
        if (
            st.session_state.lat != new_lat
            or st.session_state.lon != new_lon
        ):
            st.session_state.lat = new_lat
            st.session_state.lon = new_lon
            st.rerun()

c1, c2 = st.columns(2)
with c1:
    owner = st.text_input(
        "๐‘ค เธเธทเนเธญเน€เธเนเธฒเธเธญเธเธเธฒ",
        placeholder="เน€เธเนเธ เธเธฒเธขเธชเธกเธเธฒเธข เนเธเธ”เธต",
    )
with c2:
    note = st.text_input(
        "๐“ เธเธฑเธเธ—เธถเธ / เธซเธกเธฒเธขเน€เธซเธ•เธธ",
        placeholder="เน€เธเนเธ เธเธฑเธ”เนเธ–เธงเธฑเธเธเธฑเธเธ—เธฃเน",
    )

st.subheader("๐—บ๏ธ เนเธเธเธ—เธตเนเธงเธฑเธ”เธเธทเนเธเธ—เธตเนเธเธฒ")

if st.session_state.lat is None:
    st.info("๐“ เธเธ”เธเธธเนเธกเธ•เธณเนเธซเธเนเธเน€เธเธทเนเธญเนเธเธขเธฑเธเธเธธเธ”เธเธฑเธเธเธธเธเธฑเธ โ€ข โ๏ธ เนเธเนเธเธธเนเธก Edit เธเธเนเธเธเธ—เธตเนเน€เธเธทเนเธญเธเธขเธฑเธเธเธธเธ”เธ—เธตเนเธงเธฑเธ”เธเธดเธ” โ€ข เธเธ” ๐—‘๏ธ เน€เธเธทเนเธญเธฅเธเนเธเธงเน€เธเธ•")

if st.session_state.lat is None or st.session_state.lon is None:
    st.warning("๐“ เธเธฃเธธเธ“เธฒเธญเธเธธเธเธฒเธ•เธ•เธณเนเธซเธเนเธ GPS เธเธญเธเธญเธธเธเธเธฃเธ“เนเธเนเธญเธเนเธเนเธเธฒเธ เนเธเธเธ—เธตเนเธเธฐเนเธกเนเนเธเนเธเธดเธเธฑเธ”เธญเธเธธเธชเธฒเธงเธฃเธตเธขเนเน€เธเนเธเธเนเธฒเน€เธฃเธดเนเธกเธ•เนเธ")
    center = [0.0, 0.0]
    zoom_level = 2
else:
    center = [st.session_state.lat, st.session_state.lon]
    zoom_level = 20

m = folium.Map(
    location=center,
    zoom_start=zoom_level,
    control_scale=True,
    tiles="OpenStreetMap",
)

folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/"
          "World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles ยฉ Esri",
    name="เธ เธฒเธเธ”เธฒเธงเน€เธ—เธตเธขเธก",
    overlay=False,
    control=True,
).add_to(m)

LocateControl(
    auto_start=False,
    flyTo=True,
    keepCurrentZoomLevel=False,
    showCompass=True,
).add_to(m)

# เนเธเน FeatureGroup เน€เธ”เธตเธขเธงเธเธฑเธ Draw เน€เธเธทเนเธญเนเธซเนเนเธเธงเน€เธเธ•เน€เธ”เธดเธกเนเธเนเนเธเนเธ”เนเธเธฃเธดเธ
drawn_items = folium.FeatureGroup(name="เนเธเธงเน€เธเธ•เนเธเธฅเธเธเธฒ", show=True)
drawn_items.add_to(m)

if len(st.session_state.points) >= 3:
    folium.Polygon(
        locations=st.session_state.points,
        color="#00b950",
        weight=5,
        fill=True,
        fill_color="#00b950",
        fill_opacity=0.18,
        tooltip="เนเธเธงเน€เธเธ•เนเธเธฅเธเธเธฒ โ€ข เนเธเนเธเธธเนเธก โ๏ธ เน€เธเธทเนเธญเนเธเนเนเธ",
    ).add_to(drawn_items)

Draw(
    export=False,
    feature_group=drawn_items,
    position="topleft",
    draw_options={
        "polyline": False,
        "rectangle": False,
        "circle": False,
        "circlemarker": False,
        "marker": False,
        "polygon": {
            "allowIntersection": False,
            "showArea": True,
            "shapeOptions": {
                "color": "#00b950",
                "weight": 4,
                "fillColor": "#00b950",
                "fillOpacity": 0.18,
            },
        },
    },
    edit_options={"edit": True, "remove": True},
).add_to(m)

map_data = st_folium(
    m,
    width=None,
    height=650,
    returned_objects=["all_drawings"],
    key="ta_map",
)

if map_data and map_data.get("all_drawings") is not None:
    new_points = get_polygon(map_data["all_drawings"])
    if new_points != st.session_state.points:
        st.session_state.points = new_points
        st.rerun()

b1, b2 = st.columns(2)
with b1:
    if st.button("๐—‘๏ธ เธฅเนเธฒเธเนเธเธงเน€เธเธ•", use_container_width=True):
        st.session_state.points = []
        st.rerun()
with b2:
    if st.button("๐” เธฃเธตเน€เธเธฃเธเนเธเธเธ—เธตเน", use_container_width=True):
        st.rerun()

area_m2 = polygon_area_m2(st.session_state.points)
rai, ngan, wa, remain_m2 = thai_area(area_m2)
plow_cost = area_m2 / RAI_M2 * PLOW_RATE
mill_cost = area_m2 / RAI_M2 * MILL_RATE
total_cost = plow_cost + mill_cost

st.divider()
st.subheader("๐“ เธเธฅเธเธฒเธฃเธงเธฑเธ”เธเธทเนเธเธ—เธตเน")

if len(st.session_state.points) < 3:
    st.warning("เธเธฃเธธเธ“เธฒเธงเธฒเธ”เธเธญเธเน€เธเธ•เนเธเธฅเธเธเธฒเธญเธขเนเธฒเธเธเนเธญเธข 3 เธเธธเธ”")
else:
    a1, a2, a3, a4 = st.columns(4)
    a1.metric("เธเธทเนเธเธ—เธตเนเธฃเธงเธก", f"{area_m2:,.2f} เธ•เธฃ.เธก.")
    a2.metric("เนเธฃเน", f"{rai:,}")
    a3.metric("เธเธฒเธ", f"{ngan:,}")
    a4.metric("เธ•เธฒเธฃเธฒเธเธงเธฒ", f"{wa:,}")

    st.success(
        f"เธเธทเนเธเธ—เธตเนเธเธฃเธฐเธกเธฒเธ“ {rai} เนเธฃเน {ngan} เธเธฒเธ {wa} เธ•เธฒเธฃเธฒเธเธงเธฒ "
        f"{remain_m2:.2f} เธ•เธฃ.เธก."
    )

    st.subheader("๐’ฐ เธขเธญเธ”เธ—เธตเนเธ•เนเธญเธเธเนเธฒเธข")
    p1, p2, p3 = st.columns(3)
    p1.metric("1๏ธโฃ เธเนเธฒเนเธ–เธเธฒ", f"{money(plow_cost)} เธเธฒเธ—")
    p2.metric("2๏ธโฃ เธเนเธฒเธเธฑเนเธเธ”เธดเธ", f"{money(mill_cost)} เธเธฒเธ—")
    p3.metric("3๏ธโฃ เธฃเธงเธกเนเธ–เธเธฒ + เธเธฑเนเธเธ”เธดเธ", f"{money(total_cost)} เธเธฒเธ—")

    st.caption("เธญเธฑเธ•เธฃเธฒเธเนเธฒเธเธฃเธดเธเธฒเธฃ: เนเธ–เธเธฒ 250 เธเธฒเธ—/เนเธฃเน โ€ข เธเธฑเนเธเธ”เธดเธ 350 เธเธฒเธ—/เนเธฃเน")

    st.markdown(
        f"""
        <div class="total-box">
            <div>๐’ฐ เธขเธญเธ”เธฃเธงเธกเธ—เธฑเนเธเธซเธกเธ”</div>
            <div class="total-money">{money(total_cost)} เธเธฒเธ—</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### ๐ฐ๏ธ เธ เธฒเธเธเธทเนเธเธ—เธตเนเธ—เธตเนเธเธณเธฅเธฑเธเธเธฐเธเธฑเธเธ—เธถเธ")
    preview = make_snapshot(st.session_state.points)
    if preview is not None:
        st.image(preview, caption="เธ เธฒเธเธ”เธฒเธงเน€เธ—เธตเธขเธกเธเธฃเนเธญเธกเนเธเธงเน€เธเธ•เนเธเธฅเธเธ—เธตเนเธงเธฑเธ”", use_container_width=True)
    else:
        st.warning("เธขเธฑเธเธชเธฃเนเธฒเธเธ เธฒเธเธ”เธฒเธงเน€เธ—เธตเธขเธกเนเธกเนเนเธ”เน เนเธ•เนเธเนเธญเธกเธนเธฅเธเธดเธเธฑเธ”เนเธฅเธฐเธเธทเนเธเธ—เธตเนเธขเธฑเธเธชเธฒเธกเธฒเธฃเธ–เธเธฑเธเธ—เธถเธเนเธ”เน")

    if st.button(
        "๐’พ เธเธฑเธเธ—เธถเธเธเนเธญเธกเธนเธฅ + เธ เธฒเธเธเธทเนเธเธ—เธตเน",
        type="primary",
        use_container_width=True,
    ):
        snapshot = preview if preview is not None else make_snapshot(st.session_state.points)

        record = {
            "เธฅเธณเธ”เธฑเธ": len(st.session_state.saved_plots) + 1,
            "เธงเธฑเธเธ—เธตเนเธเธฑเธเธ—เธถเธ": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "เน€เธเนเธฒเธเธญเธเธเธฒ": owner.strip() or "-",
            "เธซเธกเธฒเธขเน€เธซเธ•เธธ": note.strip() or "-",
            "เธเธทเนเธเธ—เธตเน_เธ•เธฃเธก": round(area_m2, 2),
            "เนเธฃเน": rai,
            "เธเธฒเธ": ngan,
            "เธ•เธฒเธฃเธฒเธเธงเธฒ": wa,
            "เน€เธซเธฅเธทเธญ_เธ•เธฃเธก": round(remain_m2, 2),
            "เธเนเธฒเนเธ–เธเธฒ": round(plow_cost, 2),
            "เธเนเธฒเธเธฑเนเธเธ”เธดเธ": round(mill_cost, 2),
            "เธฃเธงเธก": round(total_cost, 2),
            "เธเธดเธเธฑเธ”": [
                [round(lat, 7), round(lon, 7)]
                for lat, lon in st.session_state.points
            ],
            "เธ เธฒเธเธเธทเนเธเธ—เธตเน_base64": image_to_base64(snapshot),
        }

        st.session_state.saved_plots.append(record)
        save_saved(st.session_state.saved_plots)
        st.success("เธเธฑเธเธ—เธถเธเน€เธฃเธตเธขเธเธฃเนเธญเธขเนเธฅเนเธงเธเธฃเธฑเธ เธเนเธญเธกเธนเธฅเธเธฐเธขเธฑเธเธญเธขเธนเนเน€เธกเธทเนเธญเธเธดเธ”เนเธฅเธฐเน€เธเธดเธ”เนเธญเธเนเธซเธกเน ๐พ")

st.divider()
st.subheader("๐“ เธเนเธญเธกเธนเธฅเนเธเธฅเธเธเธฒเธ—เธตเนเธเธฑเธเธ—เธถเธเนเธงเน")

if not st.session_state.saved_plots:
    st.info("เธขเธฑเธเนเธกเนเธกเธตเธเนเธญเธกเธนเธฅเธ—เธตเนเธเธฑเธเธ—เธถเธ")
else:
    for item in reversed(st.session_state.saved_plots):
        title = (
            f"เนเธเธฅเธเธ—เธตเน {item['เธฅเธณเธ”เธฑเธ']} โ€ข "
            f"{item['เน€เธเนเธฒเธเธญเธเธเธฒ']} โ€ข "
            f"{money(item['เธฃเธงเธก'])} เธเธฒเธ—"
        )
        with st.expander(title):
            left, right = st.columns([1.2, 1])

            with left:
                saved_image = base64_to_image(
                    item.get("เธ เธฒเธเธเธทเนเธเธ—เธตเน_base64")
                )
                if saved_image is not None:
                    st.image(
                        saved_image,
                        caption="เธ เธฒเธเธเธทเนเธเธ—เธตเนเนเธเธฅเธเธเธฒเธ—เธตเนเธเธฑเธเธ—เธถเธเนเธงเน",
                        use_container_width=True,
                    )
                else:
                    st.warning("เนเธกเนเธเธเธ เธฒเธเธเธญเธเนเธเธฅเธเธเธตเน")

            with right:
                st.write(f"**เน€เธเนเธฒเธเธญเธเธเธฒ:** {item['เน€เธเนเธฒเธเธญเธเธเธฒ']}")
                st.write(f"**เธงเธฑเธเธ—เธตเนเธเธฑเธเธ—เธถเธ:** {item['เธงเธฑเธเธ—เธตเนเธเธฑเธเธ—เธถเธ']}")
                st.write(f"**เธซเธกเธฒเธขเน€เธซเธ•เธธ:** {item['เธซเธกเธฒเธขเน€เธซเธ•เธธ']}")
                st.write(
                    f"**เธเธทเนเธเธ—เธตเน:** {item['เนเธฃเน']} เนเธฃเน "
                    f"{item['เธเธฒเธ']} เธเธฒเธ {item['เธ•เธฒเธฃเธฒเธเธงเธฒ']} เธ•เธฒเธฃเธฒเธเธงเธฒ "
                    f"{item['เน€เธซเธฅเธทเธญ_เธ•เธฃเธก']:.2f} เธ•เธฃ.เธก."
                )
                st.write(f"**เธเนเธฒเนเธ–เธเธฒ:** {money(item['เธเนเธฒเนเธ–เธเธฒ'])} เธเธฒเธ—")
                st.write(f"**เธเนเธฒเธเธฑเนเธเธ”เธดเธ:** {money(item['เธเนเธฒเธเธฑเนเธเธ”เธดเธ'])} เธเธฒเธ—")
                st.write(f"**เธฃเธงเธก:** {money(item['เธฃเธงเธก'])} เธเธฒเธ—")

                export_item = dict(item)
                export_item.pop("เธ เธฒเธเธเธทเนเธเธ—เธตเน_base64", None)

                st.download_button(
                    "โฌ๏ธ เธ”เธฒเธงเธเนเนเธซเธฅเธ”เธเนเธญเธกเธนเธฅเนเธเธฅเธเธเธตเน",
                    data=json.dumps(
                        export_item,
                        ensure_ascii=False,
                        indent=2,
                    ).encode("utf-8"),
                    file_name=f"ta_plot_{item['เธฅเธณเธ”เธฑเธ']}.json",
                    mime="application/json",
                    use_container_width=True,
                    key=f"download_{item['เธฅเธณเธ”เธฑเธ']}",
                )

    export_all = []
    for item in st.session_state.saved_plots:
        row = dict(item)
        row.pop("เธ เธฒเธเธเธทเนเธเธ—เธตเน_base64", None)
        export_all.append(row)

    st.download_button(
        "โฌ๏ธ เธ”เธฒเธงเธเนเนเธซเธฅเธ”เธเนเธญเธกเธนเธฅเธ—เธฑเนเธเธซเธกเธ”",
        data=json.dumps(
            export_all,
            ensure_ascii=False,
            indent=2,
        ).encode("utf-8"),
        file_name="ta_plots.json",
        mime="application/json",
        use_container_width=True,
    )

st.divider()
st.caption(
    "Ta App โ€ข เน€เธเธดเธ”เนเธเนเธเธฒเธเธซเธเนเธฒเธเธฒเธเธ”เนเธงเธข GPS เธเธญเธเน€เธเธฃเธทเนเธญเธเธ—เธตเนเน€เธเธดเธ”เนเธญเธ "
    "โ€ข เธเนเธญเธกเธนเธฅเธ—เธตเนเธเธฑเธเธ—เธถเธเน€เธเนเธเนเธ ta_data.json เธเธเน€เธเธฃเธทเนเธญเธ/เน€เธเธดเธฃเนเธเน€เธงเธญเธฃเนเธ—เธตเนเธฃเธฑเธเนเธญเธ "
    "โ€ข เธเนเธฒเธเธทเนเธเธ—เธตเนเน€เธเนเธเธเนเธฒเธเธฃเธฐเธกเธฒเธ“เธเธฒเธเธเธดเธเธฑเธ” GPS"
  )
