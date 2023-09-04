document.addEventListener("DOMContentLoaded", function() {
    const uploadForm = document.getElementById('upload-form');
    const fileInput = document.getElementById('fileInput');
    const results = document.getElementById('results');
  
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const file = fileInput.files[0];
        const submitButton = document.getElementById('submit-button');
        const uploadSection = document.getElementById('upload-section');
    
        submitButton.disabled = true;
        submitButton.innerText = "Procesando...";
  
      if (file && (file.type === "application/pdf" || file.type === "text/plain")) {
        const formData = new FormData();
        formData.append("file", file);
  
        try {
          const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
          });
  
          if (response.ok) {
            const data = await response.json();
            const formattedResult = formatResults(data); // Utilizar la función para formatear los resultados
            results.style.display = "block";
            results.innerHTML = `<h2>Resultado</h2>${formattedResult}`;
          } else {
            results.style.display = "block";
            results.innerHTML = `<h2>Error</h2><p>Algo salió mal en el servidor</p>`;
          }
        } catch (error) {
          results.style.display = "block";
          results.innerHTML = `<h2>Error</h2><p>${error.toString()}</p>`;
        }
      } else {
        results.style.display = "block";
        results.innerHTML = `<h2>Error</h2><p>Archivo no válido. Asegúrate de subir un PDF o un archivo de texto.</p>`;
      }
      
      submitButton.disabled = false;
      submitButton.innerText = "Empieza Ahora";
  
    });
  });
  
  // La otra parte de tu código que se ocupa de los faqToggles no necesita cambios, así que la dejamos como está
  document.addEventListener("DOMContentLoaded", function() {
    const faqToggles = document.querySelectorAll('.faq-toggle');
    
    faqToggles.forEach((toggle) => {
      toggle.addEventListener('click', (event) => {
        const content = event.currentTarget.nextElementSibling;
        content.classList.toggle('open');
      });
    });
  });
  
  function formatResults(data) {
    let content = data.result;  // Cambio a 'result' ya que es la clave donde se guarda el resultado en tu JSON
    let sections = content.split("\n\n");  // Suponiendo que cada sección está separada por dos saltos de línea
    let formattedSections = sections.map(section => {
      let [title, ...text] = section.split('\n');
      let joinedText = text.join(' ');
      return `
        <div class='result-section'>
          <h3>${title}</h3>
          <p>${joinedText}</p>
        </div>`;
    }).join('');
  
    return `
      <div class='results-container'>
        ${formattedSections}
      </div>`;
  }
  