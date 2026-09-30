/**
 * AcadAssist - Academic Services Inquiry & Booking Manager
 */

const ServiceInquiryManager = {
  openInquiryModal(serviceName = 'Handwritten Work', defaultPrice = '₹15/page') {
    const modal = document.getElementById('service-order-modal');
    if (!modal) return;

    const titleEl = document.getElementById('service-order-title');
    const categoryInput = document.getElementById('service-order-category');
    const priceBadge = document.getElementById('service-order-price-badge');

    if (titleEl) titleEl.textContent = `Order ${serviceName}`;
    if (categoryInput) categoryInput.value = serviceName;
    if (priceBadge) priceBadge.textContent = defaultPrice;

    // Autofill with logged in user if available
    if (window.AuthManager && window.AuthManager.currentUser) {
      const u = window.AuthManager.currentUser;
      const nameInput = document.getElementById('service-order-name');
      const phoneInput = document.getElementById('service-order-phone');
      const emailInput = document.getElementById('service-order-email');
      if (nameInput && !nameInput.value) nameInput.value = u.name;
      if (phoneInput && !phoneInput.value) phoneInput.value = u.phone;
      if (emailInput && !emailInput.value) emailInput.value = u.email;
    }

    modal.showModal();
  },

  async submitInquiry(e) {
    e.preventDefault();
    const category = document.getElementById('service-order-category')?.value || 'General Academic Assistance';
    const name = document.getElementById('service-order-name')?.value.trim();
    const phone = document.getElementById('service-order-phone')?.value.trim();
    const email = document.getElementById('service-order-email')?.value.trim();
    const topic = document.getElementById('service-order-topic')?.value.trim();
    const details = document.getElementById('service-order-details')?.value.trim();
    const deadline = document.getElementById('service-order-deadline')?.value;

    const submitBtn = document.getElementById('service-order-submit-btn');
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = `Sending to AcadAssist Team...`;
    }

    try {
      const res = await fetch('/api/services/inquiry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          service_category: category,
          student_name: name,
          phone: phone,
          email: email,
          details: details,
          subject_or_topic: topic,
          deadline: deadline
        })
      });

      const data = await res.json();
      if (res.ok) {
        document.getElementById('service-order-modal')?.close();
        
        // Open WhatsApp directly with prefilled order details
        const waMsg = `Hi AcadAssist, I want to book *${category}* for *${topic || 'Coursework'}*.\n\nMy Details:\n• Name: ${name}\n• Phone: ${phone}\n• Deadline: ${deadline || 'Flexible'}\n• Details: ${details}\n\nPlease confirm availability!`;
        window.open(`https://wa.me/917719730804?text=${encodeURIComponent(waMsg)}`, '_blank');

        alert(`✅ Your inquiry for ${category} has been received! Our support team will connect with you on WhatsApp shortly.`);
      }
    } catch (err) {
      alert("Failed to submit request. Please reach out to us directly on WhatsApp (+91 7719730804).");
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = `Submit Order & Chat on WhatsApp →`;
      }
    }
  }
};

window.ServiceInquiryManager = ServiceInquiryManager;
