import { Button } from "@/components/ui/button";

const links = {
  NL: "https://lookerstudio.google.com/s/q_XrQiH9dFs",
  EN: "https://lookerstudio.google.com/s/oTJUoLI7MrY",
};

const ReferencePage = () => {
  return (
    <div className="flex justify-center items-center min-h-screen gap-4">
      <div className="grid gird-cols-1 gap-4">
        <h2 className="text-xl font-semibold text-center mb-4">
          Select to which dashboard you want to go
        </h2>
        <Button asChild>
          <a href={links.NL} target="_blank" rel="noopener noreferrer">
            Dutch
          </a>
        </Button>
        <Button asChild>
          <a href={links.EN} target="_blank" rel="noopener noreferrer">
            English
          </a>
        </Button>
      </div>
    </div>
  );
};

export default ReferencePage;
