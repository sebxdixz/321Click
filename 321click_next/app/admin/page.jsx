"use client";
import { useForm } from "react-hook-form";
import { useRouter } from "next/navigation";


function RegisterPage() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const router = useRouter();

  const onSubmit = handleSubmit(async (data) => {

    const res = await fetch("localhost:4000/trabajo", {
      method: "POST",
      body: JSON.stringify({
        nom_trabajo: data.nom_trabajo,
        desc_trabajo: data.descripcion_trabajo,
        pago: data.pago,
        estado:"Disponible",
        rut_empleador1:208331302,
        fecha_comienzo: data.fecha_comienzo,
        fecha_final:data.fecha_final

      }),
      headers: {
        "Content-Type": "application/json",
      },
    });

    if (res.ok) {
      router.push("/trabajo");
    }
  });

  console.log(errors);

  return (
    <div className="h-[calc(100vh-7rem)] flex justify-center items-center">
      <form onSubmit={onSubmit} className="w-1/4">
        <h1 className="text-slate-200 font-bold text-4xl mb-4">Publica un nuevo trabajo</h1>

        <label htmlFor="nom_trabajo" className="text-slate-500 mb-2 block text-sm">
          nombre del trabajo:
        </label>
        <input
          type="text"
          {...register("username", {
            required: {
              value: true,
              message: "Campo requerido",
            },
          })}
          className="p-3 rounded block mb-2 bg-slate-900 text-slate-300 w-full"
          placeholder="trabajo X"
        />



        <label htmlFor="desc_trabajo" className="text-slate-500 mb-2 block text-sm">
          descripcion del trabajo:
        </label>
        <input
          type="text"
          {...register("text", {
            required: {
              value: true,
              message: "Campo requerido",
            },
          })}
          className="p-3 rounded block mb-2 bg-slate-900 text-slate-300 w-full"
          placeholder="descripcion del trabajo..."
        />


        <label htmlFor="Pago" className="text-slate-500 mb-2 block text-sm">
          Pago del trabajo:
        </label>
        <input
          type="int"
          {...register("int", {
            required: {
              value: true,
              message: "Campo requerido",
            },
          })}
          className="p-3 rounded block mb-2 bg-slate-900 text-slate-300 w-full"
          placeholder="$14.990"
        />


<label htmlFor="fecha_comienzo" className="text-slate-500 mb-2 block text-sm">
          Fecha de inicio:
        </label>
        <input
          type="date"
          {...register("date", {
            required: {
              value: true,
              message: "Campo requerido",
            },
          })}
          className="p-3 rounded block mb-2 bg-slate-900 text-slate-300 w-full"
          placeholder="11/22/2023"
        />


<label htmlFor="fecha_final" className="text-slate-500 mb-2 block text-sm">
          Fecha final:
        </label>
        <input
          type="date"
          {...register("date", {
            required: {
              value: true,
              message: "Campo requerido",
            },
          })}
          className="p-3 rounded block mb-2 bg-slate-900 text-slate-300 w-full"
          placeholder="11/22/2023"
        />


        <button className="w-full bg-blue-500 text-white p-3 rounded-lg mt-2">
          Publicar trabajo
        </button>
      </form>
      
    </div>
  );
}


export default RegisterPage;