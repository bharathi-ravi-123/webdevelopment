document.addEventListener("DOMContentLoaded", function () {
    const params = new URLSearchParams(window.location.search);
    const course = params.get("course") || "Unknown Course";

    
    const decodedCourse = decodeURIComponent(course);

    const coursePrices = {
        "Web Development": 4599,
        "UI & UX Design": 3999,
        "AIML": 5999,
        "Digital Marketing": 1999,
        "Cyber Security": 1299,
        "Data Science": 5999,
        "Power BI": 1599,
        "Advance Python": 1999,
        "Deep Learning": 7999
    };

    const coursePrice = coursePrices[decodedCourse] || 4999;

    document.getElementById("courseName").innerText = decodedCourse;
    document.getElementById("price").innerText = coursePrice;
    document.getElementById("payBtn").innerText = `🔒 Pay ₹${coursePrice}`;

    document.getElementById("payBtn").onclick = function () {
        const name = document.getElementById("studentName").value;
        const email = document.getElementById("studentEmail").value;

        if (!name || !email) {
            alert("Please enter your name and email.");
            return;
        }

        const options = {
            key: "rzp_test_u5LGP8I982QnSp",
            amount: coursePrice * 100,
            currency: "INR",
            name: "Tagore Trust",
            description: `${decodedCourse} Course Payment`,
            handler: function (response) {
                const paymentId = response.razorpay_payment_id;

                fetch("/store_payment", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        payment_id: paymentId,
                        course: decodedCourse,
                        name: name,
                        email: email
                    })
                })
                .then(res => res.json())
                .then(data => {
                    console.log(data.message);
                    window.location.href = "/success";
                })
                .catch(err => {
                    alert("⚠️ Payment was successful, but saving failed.");
                    console.error("Saving error:", err);
                });
            },
            prefill: {
                name: name,
                email: email
            },
            theme: {
                color: "#805ad5"
            }
        };

        const rzp = new Razorpay(options);
        rzp.open();
    };
});




