
function read_template(filename)
    filepath = string("./templates/", filename)
    stream = filename != nothing ? open(filepath, "r") : STDIN
    template = readline(stream)
    close(stream)
    return template
end

function create_generation_func(record_type::UTF8String, record_args::Array{UTF8String, 1})
    if record_type == "generic"
        template = read_template("generic.template")
        tfmt = "%a %b %d %H:%M:%S %Y"

        @eval f(i32,ui32,f32,vc,ts,x,y) = @printf(STDOUT, $template, i32, ui32, f32, vc, ts, x, y)
        gen_func = function (N)
            for i in 1:N
                i32 = rand(Int32)
                ui32 = rand(Uint32)
                f32 = rand(Float32)*100000
                vc = randstring()
                ts = strftime(tfmt, rand(Int32))
                x = (360.0 * rand()) - 180.0
                y = (180.0 * acos(2.0 * rand() - 1.0) / pi - 90.0)

                f(i32,ui32,f32,vc,ts,x,y)
            end
        end
    end

    gen_func
end

function main()
    if length(ARGS) < 2
         println("generate.jl <num-recs> <record-type> [<arg-1>..<arg-n>]")
         exit(1)
    end
    
    # pull arguments from the command line
    N = int(ARGS[1])
    record_type = ARGS[2]
    record_args = ARGS[3:end]

    g = create_generation_func(record_type, record_args)

    g(N)
end

main()

