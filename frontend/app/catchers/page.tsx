import Sidebar from "@/components/Sidebar";

export default function HittersPage() {
  const hitters = [
    { name: "John Doe", team: "Tigers", avg: ".312", obp: ".395", slg: ".521", ops: ".916", pa: 412 },
    { name: "Alex Smith", team: "Bears", avg: ".287", obp: ".356", slg: ".468", ops: ".824", pa: 389 },
    { name: "Sam Lee", team: "Wolves", avg: ".265", obp: ".338", slg: ".402", ops: ".740", pa: 350 },
  ];

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center pt-20 bg-gray-900"
      style={{
        backgroundImage: `url('/aztec_cal.jpg')`,
        backgroundSize: "cover",
        backgroundPosition: "top",
      }}
    >
      {/* Overlay for darkening bg image */}
      

      {/* Content */}
      <div className="relative w-full py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 ">

          <div className="flex flex-col lg:flex-row gap-8 bg-white">
            {/* Sidebar */}
            <aside className="w-full lg:w-1/4">
              <Sidebar />
            </aside>

            {/* Main Content */}
            <main className="w-full lg:w-3/4">
              <h1 className="text-4xl md:text-6xl font-extrabold text-white tracking-tight mb-3">
                Cathers
              </h1>

              <p className="text-gray-300 text-base md:text-lg mb-10">
                View and analyze catcher performance statistics.
              </p>

              {/* Table */}
              <div className="overflow-x-auto rounded-lg shadow-lg border border-gray-700 bg-gray-800 backdrop-blur">
                <table className="min-w-full text-sm">
                  <thead className="bg-gray-800 text-gray-300 border-b border-gray-700">
                    <tr>
                      {["Name", "Team", "AVG", "OBP", "SLG", "OPS", "PA"].map((label) => (
                        <th
                          key={label}
                          className={`px-4 py-3 font-semibold ${
                            label === "Name" || label === "Team" ? "text-left" : "text-right"
                          }`}
                        >
                          {label}
                        </th>
                      ))}
                    </tr>
                  </thead>

                  <tbody className="divide-y divide-gray-700">
                    {hitters.map((h) => (
                      <tr
                        key={h.name}
                        className="hover:bg-gray-700/50 transition-colors"
                      >
                        <td className="px-4 py-3 text-gray-100">{h.name}</td>
                        <td className="px-4 py-3 text-gray-300">{h.team}</td>
                        <td className="px-4 py-3 text-right text-gray-100">{h.avg}</td>
                        <td className="px-4 py-3 text-right text-gray-100">{h.obp}</td>
                        <td className="px-4 py-3 text-right text-gray-100">{h.slg}</td>
                        <td className="px-4 py-3 text-right text-gray-100">{h.ops}</td>
                        <td className="px-4 py-3 text-right text-gray-300">{h.pa}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </main>
          </div>

        </div>
      </div>

    </div>
  );
}
