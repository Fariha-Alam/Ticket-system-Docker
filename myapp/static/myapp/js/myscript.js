<script>
        // Handle file upload display
        document.getElementById('fileUpload').addEventListener('change', function(e) {
            const fileName = e.target.files[0] ? e.target.files[0].name : 'No file chosen';
            document.querySelector('.file-name').textContent = fileName;
        });
        
        // Handle form submission
        document.getElementById('requestForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Request submitted successfully!');
            this.reset();
            document.querySelector('.file-name').textContent = 'No file chosen';
        });
        
        // Simulate dropdown for better mobile experience
        document.querySelectorAll('.dropdown-menu a').forEach(item => {
            item.addEventListener('click', function() {
                // In a real app, this would navigate to the selected page
                console.log('Navigating to:', this.textContent.trim());
            });
        });
    </script>