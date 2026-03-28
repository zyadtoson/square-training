import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add CSS
css_to_add = """
      /* ── TEAMS ── */
      .teams-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; margin-top: 16px; }
      .team-card { background: #2d2d2d; border: 1px solid #3d3d3d; border-radius: 12px; padding: 20px; }
      .team-title { font-size: 1.2rem; color: #c41818; margin-bottom: 12px; font-weight: bold; border-bottom: 1px solid #3d3d3d; padding-bottom: 8px;}
      .team-members { list-style: none; margin-bottom: 16px; }
      .team-members li { padding: 8px 0; border-bottom: 1px dashed #444; color: #ddd; font-size: 0.9rem; display: flex; align-items: center; gap: 8px; }
      .team-members li::before { content: "👤"; }
      .team-cta { background: #25D366; color: #fff; text-decoration: none; padding: 10px; border-radius: 8px; display: block; text-align: center; font-weight: bold; transition: 0.2s; }
      .team-cta:hover { background: #1ebe57; color: #fff; }
"""
if "TEAMS" not in content:
    content = content.replace('/* ── DASHBOARD SHARED ── */', css_to_add + '\n      /* ── DASHBOARD SHARED ── */')

# 2. Add teacher sidebar item
t_sidebar_target = """            <div class="nav-item" onclick="switchTab('t-analytics', this)">
              <div class="n-icon">📈</div>
              <div class="n-text">الإحصائيات</div>
            </div>"""
t_sidebar_add = """
            <div class="nav-item" onclick="switchTab('t-project', this)">
              <div class="n-icon">🚀</div>
              <div class="n-text">المشروع النهائي</div>
            </div>"""
if "t-project" not in t_sidebar_target and "t-project" not in content[:content.find('s-dash')]:
    content = content.replace(t_sidebar_target, t_sidebar_target + t_sidebar_add)

# 3. Add student sidebar item
s_sidebar_target = """            <div class="nav-item" onclick="switchTab('s-profile', this)">
              <div class="n-icon">⚙️</div>
              <div class="n-text">حسابي</div>
            </div>"""
s_sidebar_add = """
            <div class="nav-item" onclick="switchTab('s-project', this)">
              <div class="n-icon">🚀</div>
              <div class="n-text">المشروع النهائي</div>
            </div>"""
if "s-project" not in s_sidebar_target and content.count("s-project") < 3:
    content = content.replace(s_sidebar_target, s_sidebar_target + s_sidebar_add)

# 4. Add Teacher Tab Content
t_tab_content_target = """        <!-- /ANALYTICS -->"""
t_tab_content = """        <!-- /ANALYTICS -->

        <div id="t-project" class="tab-content">
          <div class="dash">
            <div class="sec-head">
              <h2 class="sec-title">🎯 تفاصيل <em>المشروع النهائي</em></h2>
            </div>
            <div class="team-card" style="margin-bottom: 24px;">
              <p style="color:#aaa; line-height:1.6;" id="t-project-desc">جاري تحضير تفاصيل المشروع والمطلوب من كل فريق... (يمكنك تزويدي بالتفاصيل المكتوبة هنا مستقبلاً)</p>
            </div>
            
            <div class="sec-head">
              <h2 class="sec-title">👥 الفرق <em>المشاركة</em></h2>
            </div>
            <div class="teams-grid" id="t-teams-container">
              <!-- Teams Rendered Here -->
            </div>
          </div>
        </div>"""
if "id=\"t-project\"" not in content:
    content = content.replace(t_tab_content_target, t_tab_content)

# 5. Add Student Tab Content
s_tab_content_target = """          </div>
        </div>
        <!-- /PROFILE -->"""
s_tab_content = """          </div>
        </div>
        <!-- /PROFILE -->

        <div id="s-project" class="tab-content">
          <div class="stu-dash">
            <div class="sec-head">
              <h2 class="sec-title">🎯 تفاصيل <em>المشروع النهائي</em></h2>
            </div>
            <div class="prog-card" style="margin-bottom: 24px;">
              <p style="color:#aaa; line-height:1.6;" id="s-project-desc">جاري التحضير لتفاصيل المشروع والمطلوب من كل فريق...</p>
            </div>
            
            <div class="sec-head">
              <h2 class="sec-title">👥 الفرق <em>المشاركة</em></h2>
            </div>
            <div class="teams-grid" id="s-teams-container">
              <!-- Teams Rendered Here -->
            </div>
          </div>
        </div>"""
if "id=\"s-project\"" not in content:
    content = content.replace(s_tab_content_target, s_tab_content)

# 6. Add Team to Modals
modal_target = """            <div class="fg">
              <label>كلمة المرور</label>"""
modal_add = """            <div class="fg">
              <label>الفريق (اختياري)</label>
              <select id="ms-team">
                <option value="">بدون فريق</option>
                <option value="Team 1">الفريق 1</option>
                <option value="Team 2">الفريق 2</option>
                <option value="Team 3">الفريق 3</option>
                <option value="Team 4">الفريق 4</option>
              </select>
            </div>
"""
if "ms-team" not in content:
    content = content.replace(modal_target, modal_add + modal_target)

# JS logic
js_logic = """
      // ====== TEAMS LOGIC ======
      const defaultTeamsMapping = {
        "احمد السيد": "Team 1", "ايه": "Team 1", "مجدي": "Team 1", "قمر": "Team 1",
        "مريم": "Team 2", "محمد": "Team 2", "كنزي": "Team 2", "نور": "Team 2", "نورين": "Team 2",
        "زينا": "Team 3", "لينا": "Team 3", "نورين باشا": "Team 3", "خالد": "Team 3",
        "أشرفت": "Team 4", "فدوى": "Team 4", "مني": "Team 4", "ليندا": "Team 4", "نادين": "Team 4"
      };

      const whatsappLinks = {
        "Team 1": "#",
        "Team 2": "#",
        "Team 3": "#",
        "Team 4": "#"
      };

      const teamNames = {
        "Team 1": "الفريق 1",
        "Team 2": "الفريق 2",
        "Team 3": "الفريق 3",
        "Team 4": "الفريق 4"
      };

      function getStudentTeam(student) {
        if (student.team) return student.team;
        for (let key in defaultTeamsMapping) {
          if (student.name && student.name.includes(key) || student.username && student.username.includes(key)) {
            return defaultTeamsMapping[key];
          }
        }
        return "";
      }

      window.renderTeamsView = function(containerId, isStudentView = false) {
        const container = g(containerId);
        if (!container) return;
        
        let teamsData = {
          "Team 1": [],
          "Team 2": [],
          "Team 3": [],
          "Team 4": []
        };
        
        students.forEach(s => {
          let t = getStudentTeam(s);
          if (t && teamsData[t]) {
            teamsData[t].push(s);
          }
        });

        let html = "";
        for (let t in teamsData) {
          let membersHtml = teamsData[t].map(s => `<li>${s.name}</li>`).join("");
          if (!membersHtml) membersHtml = "<li style='color:#777;'>لا يوجد أعضاء بعد</li>";
          
          let ctaHtml = "";
          if (isStudentView && currentUser) {
            let myTeam = getStudentTeam(currentUser);
            if (myTeam === t) {
              ctaHtml = `<a href="${whatsappLinks[t]}" target="_blank" class="team-cta" onclick="if(this.getAttribute('href')==='#') { alert('الرابط قيد التجهيز من الإدارة!'); return false; }">💬 انضم لتيمك على الواتساب</a>`;
            }
          }
          
          html += `
            <div class="team-card">
              <div class="team-title">${teamNames[t]}</div>
              <ul class="team-members">
                ${membersHtml}
              </ul>
              ${ctaHtml}
            </div>
          `;
        }
        container.innerHTML = html;
      }
"""
if "defaultTeamsMapping" not in content:
    content = content.replace("function renderTeacherDash() {", js_logic + "\n      function renderTeacherDash() {")

# Render teams in dashes
if "renderTeamsView('t-teams-container');" not in content:
    content = content.replace("tanalytics.render();", "tanalytics.render();\n        renderTeamsView('t-teams-container');")
if "renderTeamsView('s-teams-container', true);" not in content:
    content = content.replace("leaderboard.renderStudent();", "leaderboard.renderStudent();\n        renderTeamsView('s-teams-container', true);")

# Update edit student js
if "g(\"ms-uname\").value = s?.username || \"\";" in content and "ms-team" not in content.split("g(\"ms-uname\").value = s?.username || \"\";")[1]:
    content = content.replace('g("ms-pass").value = "";', 'g("ms-pass").value = "";\n        g("ms-team").value = s?.team || "";')
    
    content = content.replace('const pass = g("ms-pass").value;', 'const pass = g("ms-pass").value;\n        const team = g("ms-team").value;')
    
    content = content.replace('username: uname,', 'username: uname,\n              team: team,')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
