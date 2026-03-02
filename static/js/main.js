document.addEventListener('DOMContentLoaded', function() {
    loadAboutData();
    loadProjects();
    setupContactForm();
});

async function loadAboutData() {
    try {
        const response = await fetch('/api/about/');
        const data = await response.json();
        
        if (data.length > 0) {
            const about = data[0];
            
            // Hero section
            document.getElementById('bio').textContent = about.bio || 'Men Robbit Akademiyasi o\'quvchisiman. Zamonaviy va foydali veb-ilovalarni yaratishga qiziqaman.';
            
            if (about.profile_image) {
                document.getElementById('profileImage').src = about.profile_image;
            }
            
            // About section
            document.getElementById('fullName').textContent = about.full_name || 'Azizbek Omonov';
            document.getElementById('birthDate').textContent = about.birth_date || '2009-06-29';
            document.getElementById('address').textContent = about.address || 'Farg\'ona shahar';
            document.getElementById('education').textContent = about.education || 'Robbit Akademiyasi o\'quvchisi';
            
            // Contact section
            document.getElementById('email').textContent = about.email || 'azizbek2004uzbek@gmail.com';
            document.getElementById('phone').textContent = about.phone || '+998 33 996 36 30';
            document.getElementById('github').textContent = about.github || 'azizbek00-gif';
        }
    } catch (error) {
        console.error('Error loading about data:', error);
    }
}

async function loadProjects() {
    try {
        const response = await fetch('/api/projects/');
        const projects = await response.json();
        
        const container = document.getElementById('projectsContainer');
        container.innerHTML = '';
        
        projects.forEach(project => {
            const techs = project.technologies.split(',').map(tech => 
                `<span class="tech-tag">${tech.trim()}</span>`
            ).join('');
            
            // Icon for project (sizning rasmingiz yoki placeholder)
            const icon = project.image ? 
                `<img src="${project.image}" style="width:100%; height:100%; object-fit:cover;">` :
                `<i class="fas fa-code"></i>`;
            
            const card = document.createElement('div');
            card.className = 'project-card';
            card.innerHTML = `
                <div class="project-img">
                    ${icon}
                </div>
                <div class="project-content">
                    <h3 class="project-title">${project.title}</h3>
                    <p class="project-desc">${project.description}</p>
                    <div class="tech-tags">
                        ${techs}
                    </div>
                    <a href="${project.github_link || '#'}" target="_blank" class="project-link">
                        Batafsil <i class="fas fa-arrow-right"></i>
                    </a>
                </div>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading projects:', error);
    }
}

function setupContactForm() {
    const form = document.getElementById('contactForm');
    const statusDiv = document.getElementById('status');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            name: form.name.value,
            email: form.email.value,
            message: form.message.value
        };
        
        try {
            const response = await fetch('/api/contact/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify(formData)
            });
            
            if (response.ok) {
                statusDiv.innerHTML = '<div style="background: #28a745; color: white; padding: 10px; border-radius: 5px;">Xabaringiz yuborildi!</div>';
                form.reset();
            } else {
                statusDiv.innerHTML = '<div style="background: #dc3545; color: white; padding: 10px; border-radius: 5px;">Xatolik yuz berdi. Qayta urinib ko\'ring.</div>';
            }
        } catch (error) {
            statusDiv.innerHTML = '<div style="background: #dc3545; color: white; padding: 10px; border-radius: 5px;">Server bilan bog\'lanib bo\'lmadi.</div>';
        }
        
        setTimeout(() => {
            statusDiv.innerHTML = '';
        }, 5000);
    });
}
