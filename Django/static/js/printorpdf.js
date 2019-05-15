
function printJ() {
  window.print();
}

function pdfprint() {
		const filename  = 'form.pdf';

		html2canvas(document.getElementById('#printcontainer')).then(canvas => {
			let pdf = new jsPDF('p', 'mm', 'a4');
			pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, 211, 298);
			pdf.save(filename);
            // pdf.output('dataurlnewwindow');
		});
}
