    # YouTube Playlist ของคุณท่าน
    st.markdown("<p style='color:#FFD700;'>🎬 เพลย์ลิสต์แนะนำจาก Synapse</p>", unsafe_allow_html=True)
    components.html('<iframe width="100%" height="200" src="https://www.youtube.com/embed/videoseries?list=PL6S211I3urvpt47sv8mhbexif2YOzs2gO" frameborder="0" allowfullscreen></iframe>', height=220)
    
    st.subheader("📂 เลือกห้องเพื่อเริ่มต้น")
    c1, c2 = st.columns(2)
    if c1.button("🔴 YouTube Zone"): st.session_state.page = "red"; st.rerun()
    if c2.button("🔵 Facebook (โทรฟรี)"): st.session_state.page = "blue"; st.rerun()
    if c1.button("🟢 ห้องแชทลับ"): st.session_state.page = "green"; st.rerun()
    if c2.button("⚫ ห้อง X เรียลไทม์"): st.session_state.page = "black"; st.rerun()
    if st.button("🚪 ออกจากระบบ"): del st.session_state.user; st.rerun()

# --- ห้องสีแดง: YouTube Zone (เน้นการแชร์และดูวิดีโอ) ---
elif st.session_state.page == "red":
    set_luxury_theme("red")
    st.header("🔴 YouTube Zone: แชร์ & ดูวิดีโอ")
    if st.button("⬅️ กลับหน้าหลัก"): st.session_state.page = "home"; st.rerun()
    
    with st.expander("📝 สร้างโพสต์ YouTube ใหม่"):
        with st.form("f_red_post", clear_on_submit=True):
            msg = st.text_area("ข้อความของคุณ (บรรยายวิดีโอ)...")
            youtube_url_input = st.text_input("ลิงก์ YouTube Video (เช่น https://www.youtube.com/watch?v=dQw4w9WgXcQ)")
            
            # ตรวจสอบ YouTube URL และดึง ID
            youtube_video_id = get_youtube_id(youtube_url_input)
            
            file = st.file_uploader("แนบรูป/วิดีโออื่นๆ (ไม่บังคับ)", type=['jpg','png','mp4'])
            
            if st.form_submit_button("แชร์วิดีโอ/โพสต์"):
                if msg or youtube_url_input or file:
                    post_media_url, post_media_type = None, None

                    if youtube_video_id: # YouTube URL มีความสำคัญกว่าไฟล์แนบ
                        post_media_url = f"https://www.youtube.com/watch?v={youtube_video_id}"
                        post_media_type = 'youtube'
                    elif file:
                        path = f"red/{uuid.uuid4()}_{file.name}"
                        blob = bucket.blob(path)
                        blob.upload_from_string(file.getvalue(), content_type=file.type)
                        blob.make_public()
                        post_media_url, post_media_type = blob.public_url, ('video' if 'video' in file.type else 'image')
                    
                    db.collection('posts_red').add({
                        'user': st.session_state.user, 'text': msg,
                        'media': post_media_url, 'type': post_media_type,
                        'likes': [], 'time': get_thai_time()
                    })
                    st.success("โพสต์ของคุณถูกแชร์แล้ว!")
                    st.rerun()
                else:
                    st.warning("กรุณาใส่ข้อความ, ลิงก์ YouTube หรือแนบไฟล์")
    
    render_post_display_and_likes("red")

# --- ห้องสีฟ้า: Facebook (โทรฟรี) ---
elif st.session_state.page == "blue":
    set_luxury_theme("blue")
    st.header("🔵 Facebook & Call Free")
    if st.button("⬅️ กลับ"): st.session_state.page = "home"; st.rerun()
    
    # --- ระบบโทรฟรี PeerJS ---
    st.markdown('<div class="post-box">📞 โทรฟรีหาเพื่อน (ทดลอง)</div>', unsafe_allow_html=True)
    friends_ref = db.collection('users').stream()
    friends = [u.id for u in friends_ref if u.id != st.session_state.user]
    
    target = st.selectbox("เลือกเพื่อนที่จะโทรหา:", [""] + friends)
    if target:
        components.html(f"""
            <script src="https://unpkg.com/peerjs@1.5.2/dist/peerjs.min.js"></script>
            <div style="background: rgba(255,255,255,0.05); padding:10px; border-radius:10px; margin-bottom:10px;">
                <p style="color:white;">สถานะ: <span id="status">กำลังรอ...</span></p>
                <button id="call" style="width:100%; padding:15px; background:#28a745; color:white; border:none; border-radius:10px; font-weight:bold;">🟢 เริ่มโทรออกไป {target}</button>
                <button id="hangup" style="width:100%; padding:15px; background:#dc3545; color:white; border:none; border-radius:10px; font-weight:bold; margin-top:10px;">🔴 วางสาย</button>
                <audio id="localAudio" autoplay muted style="display:none;"></audio>
                <audio id="remoteAudio" autoplay></audio>
            </div>
            <script>
                const peer = new Peer('{st.session_state.user}');
                let currentCall = null;
                const status = document.getElementById('status');
                const remoteAudio = document.getElementById('remoteAudio');
                const localAudio = document.getElementById('localAudio');

                peer.on('open', id => {{
                    status.textContent = `เชื่อมต่อแล้ว, ID: ${id}`;
                }});

                peer.on('call', call => {{
                    status.textContent = `มีสายเรียกเข้าจาก ${call.peer}! กำลังรับ...`;
                    navigator.mediaDevices.getUserMedia({{ audio: true, video: false }})
                        .then(stream => {{
                            localAudio.srcObject = stream;
                            call.answer(stream);
                            call.on('stream', remoteStream => {{
                                remoteAudio.srcObject = remoteStream;
                                status.textContent = `กำลังสนทนากับ ${call.peer}`;
                            }});
                            call.on('close', () => {{
                                status.textContent = `สายหลุดจาก ${call.peer}`;
                                remoteAudio.srcObject = null;
                                stream.getTracks().forEach(track => track.stop());
                                currentCall = null;
                            }});
                            currentCall = call;
                        }})
                        .catch(err => {{
                            console.error("ไม่สามารถเข้าถึงไมโครโฟน: ", err);
                            status.textContent = "ปฏิเสธ: ไม่สามารถเข้าถึงไมโครโฟน";
                        }});
                }});

                peer.on('error', err => {{
                    console.error("PeerJS Error:", err);
                    status.textContent = `เกิดข้อผิดพลาด: ${err.type}`;
                });

                document.getElementById('call').onclick = () => {{
                    const targetPeerId = '{target}';
                    if (!targetPeerId) {{
                        status.textContent = "กรุณาเลือกเพื่อนที่จะโทรหา";
                        return;
                    }}
                    status.textContent = `กำลังโทรหา ${targetPeerId}...`;
                    navigator.mediaDevices.getUserMedia({{ audio: true, video: false }})
                        .then(stream => {{
                            localAudio.srcObject = stream;
                            const call = peer.call(targetPeerId, stream);
                            call.on('stream', remoteStream => {{
                                remoteAudio.srcObject = remoteStream;
                                status.textContent = `กำลังสนทนากับ ${targetPeerId}`;
                            });
                            call.on('close', () => {{
                                status.textContent = `สายหลุดจาก ${targetPeerId}`;
                                remoteAudio.srcObject = null;
                                stream.getTracks().forEach(track => track.stop());
                                currentCall = null;
                            }});
                            call.on('error', (err) => {{
                                console.error("Call Error:", err);
                                status.textContent = `เกิดข้อผิดพลาดในการโทร: ${err}`;
                                stream.getTracks().forEach(track => track.stop());
                                currentCall = null;
                            }});
                            currentCall = call;
                        }})
                        .catch(err => {{
                            console.error("ไม่สามารถเข้าถึงไมโครโฟน: ", err);
                            status.textContent = "โทรออกไม่สำเร็จ: ไม่สามารถเข้าถึงไมโครโฟน";
                        }});
                }};

                document.getElementById('hangup').onclick = () => {{
                    if (currentCall) {{
                        currentCall.close();
                        status.textContent = "วางสายแล้ว";
                        remoteAudio.srcObject = null;
                        if (localAudio.srcObject) {{
                            localAudio.srcObject.getTracks().forEach(track => track.stop());
                        }}
                        currentCall = null;
                    }}
                }};
            </script>
        """, height=350) # เพิ่มความสูงเพื่อให้มีที่สำหรับสถานะและปุ่มวางสาย
    
    # ฟอร์มสร้างโพสต์สำหรับ Facebook
    with st.expander("📝 สร้างโพสต์ใหม่"):
        with st.form("f_blue_post", clear_on_submit=True):
            msg = st.text_area("ข้อความของคุณ...")
            file = st.file_uploader("แนบรูป/วิดีโอ (ไม่บังคับ)", type=['jpg','png','mp4'])
            if st.form_submit_button("แชร์สู่ Facebook"):
                if msg or file:
                    url, f_type = None, None
                    if file:
                        path = f"blue/{uuid.uuid4()}_{file.name}"
                        blob = bucket.blob(path)
                        blob.upload_from_string(file.getvalue(), content_type=file.type)
                        blob.make_public()
                        url, f_type = blob.public_url, ('video' if 'video' in file.type else 'image')
                    
                    db.collection('posts_blue').add({
                        'user': st.session_state.user, 'text': msg,
                        'media': url, 'type': f_type,
                        'likes': [], 'time': get_thai_time()
                    })
                    st.success("โพสต์ของคุณถูกแชร์แล้ว!")
                    st.rerun()
                else:
                    st.warning("กรุณาใส่ข้อความหรือแนบไฟล์")
    
    render_post_display_and_likes("blue")

# --- ห้องสีเขียว: Secret Chat (แชทส่วนตัว) ---
elif st.session_state.page == "green":
    set_luxury_theme("green")
    st.header("🟢 Secret Chat: คุยส่วนตัว")
    if st.button("⬅️ กลับ"): st.session_state.page = "home"; st.rerun()
    
    friends_ref = db.collection('users').stream()
    friends = [u.id for u in friends_ref if u.id != st.session_state.user]
    target = st.selectbox("เลือกเพื่อนที่จะคุยด้วย:", [""] + friends)

    if target:
        # สร้าง Chat ID แบบมีมาตรฐาน (เรียงตามตัวอักษรเพื่อไม่ให้ซ้ำ)
        cid = "".join(sorted([st.session_state.user, target]))
        
        # ฟอร์มสำหรับส่งข้อความลับ
        with st.form("sc", clear_on_submit=True):
            m = st.text_input("ความลับที่อยากบอก...")
            if st.form_submit_button("ส่งลับๆ"):
                if m:
                    db.collection('s_chat').add({
                        'cid': cid,
                        'sender': st.session_state.user, # เปลี่ยน 's' เป็น 'sender' เพื่อความชัดเจน
                        'message': m,                     # เปลี่ยน 't' เป็น 'message'
                        'time': get_thai_time()
                    })
                    st.rerun()
                else:
                    st.warning("กรุณาพิมพ์ข้อความ")
        
        st.markdown("---")
        st.subheader(f"การสนทนากับ {target}")
        
        # แสดงข้อความแชท
        # ใช้ empty placeholder เพื่อให้ข้อความรีเฟรชได้โดยไม่ต้องรีเฟรชทั้งหน้า
        chat_placeholder = st.empty()
        with chat_placeholder.container():
            # ดึงข้อความล่าสุด 10 ข้อความ
            messages_ref = db.collection('s_chat').where('cid', '==', cid).order_by('time', direction='DESCENDING').limit(10).stream()
            messages = sorted([msg.to_dict() for msg in messages_ref], key=lambda x: x['time']) # เรียงลำดับจากเก่าไปใหม่
            
            for msg_data in messages:
                msg_time = msg_data['time']
                if isinstance(msg_time, datetime):
                    time_str = msg_time.strftime("%H:%M:%S")
                else:
                    time_str = msg_time.astimezone(timedelta(hours=7)).
