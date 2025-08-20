import { Sheet, Upload } from "lucide-react";

const MainPage = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-full">
      <div className="bg-background w-full text-center py-6 rounded-md ">
        <h1 className="text-3xl font-bold">Upload Your Data</h1>
      </div>

      <div className="flex flex-col h-full">
        <div className="p-8 rounded mt-8 rounded-sm">
          <h2 className="text-xl font-semibold text-center mb-4">
            How It Works
          </h2>
          <div className="flex justify-around space-x-4">
            <div className="text-center">
              <Upload className="mx-auto" size={48} />
              <h3 className="font-medium">Go to Upload</h3>
              <p className="text-gray-600">Click to visit our upload page.</p>
            </div>
            <div className="text-center">
              <Sheet className="mx-auto" size={48} />
              <h3 className="font-medium">Upload CSV</h3>
              <p className="text-gray-600">Securely upload your data file.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
