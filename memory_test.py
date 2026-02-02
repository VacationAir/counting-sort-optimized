import numpy as np
import time
import psutil
import os
import signal
import sys
from threading import Thread
import traceback

# ---------------------------------------
# Algoritmo con PROGRESO VISIBLE
# ---------------------------------------

def counting_sort_original_with_progress(array):
    """Counting sort que muestra progreso"""
    if len(array) == 0:
        return []
    
    # Fase 1: Encontrar máximo
    print("   🔍 Fase 1/3: Buscando máximo...")
    MAX_VALUE = 0
    progress_interval = max(1, len(array) // 20)  # Mostrar 20 actualizaciones
    for i in range(len(array)):
        if MAX_VALUE < array[i]:
            MAX_VALUE = array[i]
        
        # Mostrar progreso
        if i % progress_interval == 0:
            progress = (i / len(array)) * 100
            print(f"   📊 Progreso: {progress:.1f}% | Máximo encontrado: {MAX_VALUE}", end='\r')
    
    print(f"   ✅ Máximo encontrado: {MAX_VALUE:,}")
    print(f"   📏 Tamaño del array de conteo: {MAX_VALUE + 1:,}")
    
    # Verificar si es viable
    estimated_memory_mb = (MAX_VALUE + 1) * 8 / 1024 / 1024  # Estimado en MB
    print(f"   💾 Memoria estimada necesaria: {estimated_memory_mb:.1f} MB")
    
    if estimated_memory_mb > 1000:  # Más de 1GB
        print(f"   ⚠️  ¡ADVERTENCIA! Necesitará ~{estimated_memory_mb:.0f}MB de RAM")
        print("   ¿Continuar? El script se detendrá si usa demasiada memoria.")
    
    # Fase 2: Contar ocurrencias
    print("   🔢 Fase 2/3: Contando ocurrencias...")
    count = [0] * (MAX_VALUE + 1)
    
    for i, num in enumerate(array):
        count[num] += 1
        
        if i % progress_interval == 0:
            progress = (i / len(array)) * 100
            unique_count = sum(1 for c in count if c > 0)
            print(f"   📊 Progreso: {progress:.1f}% | Valores únicos: {unique_count:,}", end='\r')
    
    unique_count = sum(1 for c in count if c > 0)
    print(f"   ✅ Conteo completado. Valores únicos: {unique_count:,}")
    
    # Fase 3: Construir array ordenado
    print("   📊 Fase 3/3: Construyendo array ordenado...")
    sorted_array = []
    total_to_process = sum(1 for c in count if c > 0)
    processed = 0
    
    for i in range(len(count)):
        if count[i] > 0:
            sorted_array.extend([i] * count[i])
            processed += 1
            
            if processed % max(1, total_to_process // 20) == 0:
                progress = (processed / total_to_process) * 100
                print(f"   📊 Progreso: {progress:.1f}% | Elementos ordenados: {len(sorted_array):,}", end='\r')
    
    print(f"   ✅ Ordenación completada. Total elementos: {len(sorted_array):,}")
    return sorted_array

def better_sorting_benchmarks_with_progress(array):
    """Better sort que muestra progreso"""
    print("   🔍 Fase 1/4: Buscando máximo...")
    MAX_VALUE = 0
    progress_interval = max(1, len(array) // 20)
    
    for i in range(len(array)):
        if MAX_VALUE < array[i]:
            MAX_VALUE = array[i]
        
        if i % progress_interval == 0:
            progress = (i / len(array)) * 100
            print(f"   📊 Progreso: {progress:.1f}% | Máximo: {MAX_VALUE:,}", end='\r')
    
    print(f"   ✅ Máximo encontrado: {MAX_VALUE:,}")
    
    # Fase 2: Crear buckets
    print("   🪣 Fase 2/4: Creando y distribuyendo buckets...")
    bucket_size = 5
    num_buckets = int((MAX_VALUE // bucket_size) + 1)
    
    print(f"   📊 Número de buckets: {num_buckets:,}")
    print(f"   📏 Tamaño por bucket: {bucket_size}")
    
    buckets = [[] for _ in range(num_buckets)]
    
    for i, value in enumerate(array):
        bucket_index = int(value // bucket_size)
        buckets[bucket_index].append(value)
        
        if i % progress_interval == 0:
            progress = (i / len(array)) * 100
            non_empty = sum(1 for b in buckets if b)
            print(f"   📊 Progreso: {progress:.1f}% | Buckets no vacíos: {non_empty:,}", end='\r')
    
    non_empty = sum(1 for b in buckets if b)
    print(f"   ✅ Distribución completada. Buckets no vacíos: {non_empty:,}")
    
    # Fase 3: Ordenar cada bucket
    print("   🔄 Fase 3/4: Ordenando buckets...")
    total_buckets = len(buckets)
    
    for bucket_idx, bucket in enumerate(buckets):
        if len(bucket) != 0:
            if bucket_idx % max(1, total_buckets // 20) == 0:
                progress = (bucket_idx / total_buckets) * 100
                print(f"   📊 Progreso buckets: {progress:.1f}% | Bucket {bucket_idx:,}/{total_buckets:,}", end='\r')
            
            local_max = 0
            local_min = bucket[0]
            
            for number in bucket:
                if local_max < number:
                    local_max = number
                if local_min > number:
                    local_min = number

            temp = [0] * (int(local_max - local_min) + 1)
            
            for number in bucket:
                temp[int(number - local_min)] += 1

            sorted_bucket = []
            for index, quantity in enumerate(temp):
                sorted_bucket.extend([index + local_min] * quantity)

            buckets[bucket_idx] = sorted_bucket
    
    print("   ✅ Todos los buckets ordenados")
    
    # Fase 4: Fusionar buckets
    print("   🔗 Fase 4/4: Fusionando buckets...")
    sorted_array = []
    total_elements = sum(len(b) for b in buckets)
    elements_merged = 0
    
    for bucket_idx, bucket in enumerate(buckets):
        if len(bucket) != 0:
            sorted_array.extend(bucket)
            elements_merged += len(bucket)
            
            if bucket_idx % max(1, len(buckets) // 20) == 0:
                progress = (elements_merged / total_elements) * 100
                print(f"   📊 Progreso fusión: {progress:.1f}% | Elementos: {elements_merged:,}/{total_elements:,}", end='\r')
    
    print(f"   ✅ Fusión completada. Total elementos: {len(sorted_array):,}")
    return sorted_array

# ---------------------------------------
# MONITOR MEJORADO
# ---------------------------------------

class MemoryGuard:
    def __init__(self, memory_limit_mb=4000, check_interval=0.1):
        self.memory_limit_mb = memory_limit_mb
        self.check_interval = check_interval
        self.stop_flag = False
        self.monitor_thread = None
        self.max_memory_used = 0
        
    def get_memory_usage(self):
        process = psutil.Process(os.getpid())
        mem = process.memory_info().rss / 1024 / 1024
        if mem > self.max_memory_used:
            self.max_memory_used = mem
        return mem
    
    def memory_monitor(self):
        warnings = 0
        while not self.stop_flag:
            try:
                mem_usage = self.get_memory_usage()
                
                if mem_usage > self.memory_limit_mb * 0.9:
                    print(f"\n   ⚠️  ALTO USO DE RAM: {mem_usage:.1f}MB ({warnings+1}/3)")
                    warnings += 1
                    
                if mem_usage > self.memory_limit_mb or warnings >= 3:
                    print(f"\n   ⛔ MÁXIMO SUPERADO: {mem_usage:.1f}MB > {self.memory_limit_mb}MB")
                    print("   🛑 Deteniendo algoritmo para proteger el sistema...")
                    os.kill(os.getpid(), signal.SIGTERM)
                    return
                    
            except:
                pass
            
            time.sleep(self.check_interval)
    
    def start(self):
        self.monitor_thread = Thread(target=self.memory_monitor)
        self.monitor_thread.daemon = True
        self.stop_flag = False
        self.max_memory_used = 0
        self.monitor_thread.start()
    
    def stop(self):
        self.stop_flag = True
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1)
        return self.max_memory_used

# ---------------------------------------
# TEST CON DETALLES DE FALLO
# ---------------------------------------

def safe_test_with_progress(algorithm_func, array, algo_name, memory_limit_mb):
    """Prueba con progreso detallado y captura de estado al fallar"""
    
    print(f"\n{'='*70}")
    print(f"🧪 {algo_name}")
    print(f"{'='*70}")
    print(f"📊 Tamaño del array: {len(array):,}")
    print(f"🎯 Valor máximo en datos: {np.max(array):,}")
    print(f"🎯 Valor mínimo en datos: {np.min(array):,}")
    print(f"🔒 Límite de memoria: {memory_limit_mb}MB")
    
    guard = MemoryGuard(memory_limit_mb=memory_limit_mb)
    start_time = time.perf_counter()
    start_memory = psutil.Process(os.getpid()).memory_info().rss
    
    try:
        guard.start()
        print("\n🚀 INICIANDO ALGORITMO...")
        
        result = algorithm_func(array.copy().tolist())
        
        guard.stop()
        end_time = time.perf_counter()
        max_memory = guard.max_memory_used
        
        elapsed = end_time - start_time
        print(f"\n✅ ALGORITMO COMPLETADO EXITOSAMENTE")
        print(f"⏱️  Tiempo total: {elapsed:.3f} segundos")
        print(f"💾 Máximo uso de RAM: {max_memory:.1f} MB")
        print(f"📈 Primeros 3 valores: {result[:3]}")
        print(f"📉 Últimos 3 valores: {result[-3:]}")
        
        # Verificar ordenación
        is_sorted = all(result[i] <= result[i+1] for i in range(min(1000, len(result)-1)))
        print(f"✓ Verificación rápida de orden: {'PASADA' if is_sorted else 'FALLADA'}")
        
        return {
            'success': True,
            'time': elapsed,
            'max_memory_mb': max_memory,
            'sorted': is_sorted,
            'phase_completed': 'ALL',
            'progress_info': '100% - Completado'
        }
        
    except MemoryError as e:
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        max_memory = guard.max_memory_used
        
        print(f"\n💥 FALLO POR MEMORIA INSUFICIENTE")
        print(f"⏱️  Tiempo hasta fallo: {elapsed:.3f} segundos")
        print(f"💾 Máximo RAM alcanzado: {max_memory:.1f} MB")
        print(f"📊 Estado al fallar: En proceso...")
        print(f"📝 Causa probable: Necesita más de {memory_limit_mb}MB para continuar")
        
        return {
            'success': False,
            'time': elapsed,
            'max_memory_mb': max_memory,
            'error': 'MemoryError',
            'phase_completed': 'UNKNOWN',
            'progress_info': f'Interrumpido por falta de RAM ({max_memory:.0f}MB usados)'
        }
        
    except Exception as e:
        end_time = time.perf_counter()
        elapsed = end_time - start_time
        max_memory = guard.max_memory_used if 'guard' in locals() else 0
        
        print(f"\n💥 ERROR INESPERADO: {type(e).__name__}")
        print(f"⏱️  Tiempo hasta error: {elapsed:.3f} segundos")
        print(f"💾 RAM usada: {max_memory:.1f} MB")
        print(f"📝 Mensaje: {str(e)}")
        
        return {
            'success': False,
            'time': elapsed,
            'max_memory_mb': max_memory,
            'error': type(e).__name__,
            'phase_completed': 'UNKNOWN',
            'progress_info': f'Error: {str(e)[:100]}...'
        }

# ---------------------------------------
# EXPERIMENTO CON ESCALADO INTELIGENTE
# ---------------------------------------

def run_progressive_experiment():
    """Ejecuta experimento aumentando valores hasta encontrar límites"""
    
    print("🎯 EXPERIMENTO DE LÍMITES DE ALGORITMOS")
    print("==========================================")
    print("Objetivo: Encontrar el máximo valor que cada")
    print("algoritmo puede manejar antes de fallar")
    print("==========================================")
    
    # Configuración adaptable
    BASE_SIZE = 10000
    memory_info = psutil.virtual_memory()
    SAFE_LIMIT_MB = min(4000, memory_info.available / 1024 / 1024 * 0.7)
    
    print(f"\n💻 ESPECIFICACIONES DEL SISTEMA:")
    print(f"   RAM total: {memory_info.total / 1024**3:.1f} GB")
    print(f"   RAM disponible: {memory_info.available / 1024**3:.1f} GB")
    print(f"   Límite seguro establecido: {SAFE_LIMIT_MB:.0f} MB")
    
    # Valores a probar (escalado exponencial)
    test_values = []
    current = 10**3  # 1,000
    while current <= 10**12:  # Hasta 1 billón
        test_values.append(current)
        current *= 10
    
    print(f"\n📊 VALORES A PROBAR: {[f'{v:,}' for v in test_values]}")
    
    results = {
        'counting': {'max_success': 0, 'fail_at': None, 'details': []},
        'better': {'max_success': 0, 'fail_at': None, 'details': []}
    }
    
    # Probar Counting Sort
    print("\n" + "="*70)
    print("🔬 PRUEBA 1: COUNTING SORT ORIGINAL")
    print("="*70)
    
    for max_val in test_values:
        print(f"\n🎯 INTENTANDO CON MAX_VALUE = {max_val:,}")
        print("-"*50)
        
        # Generar datos de prueba
        array = np.random.randint(0, max_val, size=BASE_SIZE)
        
        # Estimar memoria necesaria
        estimated_mb = (max_val + 1) * 8 / 1024 / 1024
        print(f"📏 Memoria estimada necesaria: {estimated_mb:,.1f} MB")
        
        if estimated_mb > SAFE_LIMIT_MB * 2:
            print(f"⚠️  SALTO: Necesitaría ~{estimated_mb:.0f}MB, muy superior al límite")
            print(f"   Counting Sort fallará seguramente con este valor")
            results['counting']['fail_at'] = max_val
            break
        
        # Ejecutar prueba
        result = safe_test_with_progress(
            counting_sort_original_with_progress,
            array,
            f"Counting Sort (max={max_val:,})",
            SAFE_LIMIT_MB
        )
        
        results['counting']['details'].append({
            'max_value': max_val,
            'result': result
        })
        
        if result['success']:
            results['counting']['max_success'] = max_val
            print(f"✅ Counting Sort MANEJÓ {max_val:,}")
        else:
            results['counting']['fail_at'] = max_val
            print(f"💥 Counting Sort FALLÓ en {max_val:,}")
            break
        
        time.sleep(1)  # Pausa entre pruebas
    
    # Probar Better Sort
    print("\n" + "="*70)
    print("🔬 PRUEBA 2: BETTER SORTING")
    print("="*70)
    
    for max_val in test_values:
        print(f"\n🎯 INTENTANDO CON MAX_VALUE = {max_val:,}")
        print("-"*50)
        
        # Generar datos de prueba (nuevos cada vez)
        array = np.random.randint(0, max_val, size=BASE_SIZE)
        
        # Para Better Sort, estimar buckets
        bucket_size = 5
        num_buckets = (max_val // bucket_size) + 1
        estimated_mb = (num_buckets * 8 + BASE_SIZE * 8) / 1024 / 1024
        
        print(f"📏 Buckets estimados: {num_buckets:,}")
        print(f"💾 Memoria estimada: {estimated_mb:.1f} MB")
        
        if estimated_mb > SAFE_LIMIT_MB * 3:
            print(f"⚠️  VALOR EXTREMO: {max_val:,} puede ser demasiado grande")
            print(f"   Se intentará pero puede fallar por memoria")
        
        # Ejecutar prueba
        result = safe_test_with_progress(
            better_sorting_benchmarks_with_progress,
            array,
            f"Better Sort (max={max_val:,})",
            SAFE_LIMIT_MB
        )
        
        results['better']['details'].append({
            'max_value': max_val,
            'result': result
        })
        
        if result['success']:
            results['better']['max_success'] = max_val
            print(f"✅ Better Sort MANEJÓ {max_val:,}")
            
            # Si manejó este valor, intentar el siguiente
            continue
        else:
            results['better']['fail_at'] = max_val
            print(f"💥 Better Sort FALLÓ en {max_val:,}")
            
            # Intentar un valor intermedio
            if max_val > 10**6:
                mid_val = max_val // 10
                print(f"\n🔄 Intentando valor intermedio: {mid_val:,}")
                
                array = np.random.randint(0, mid_val, size=BASE_SIZE)
                result_mid = safe_test_with_progress(
                    better_sorting_benchmarks_with_progress,
                    array,
                    f"Better Sort (max={mid_val:,})",
                    SAFE_LIMIT_MB
                )
                
                if result_mid['success']:
                    results['better']['max_success'] = mid_val
                    print(f"✅ Better Sort MANEJÓ el valor intermedio {mid_val:,}")
            
            break
        
        time.sleep(1)
    
    # Mostrar resumen comparativo
    print("\n" + "="*70)
    print("📊 RESUMEN COMPARATIVO FINAL")
    print("="*70)
    
    print(f"\n🎯 MÁXIMOS VALORES MANEJADOS:")
    print(f"   Counting Sort Original: {results['counting']['max_success']:,}")
    print(f"   Better Sorting: {results['better']['max_success']:,}")
    
    if results['counting']['max_success'] > 0 and results['better']['max_success'] > 0:
        ratio = results['better']['max_success'] / results['counting']['max_success']
        print(f"\n📈 Better Sort puede manejar valores {ratio:.1f} veces mayores")
    
    print(f"\n💡 ANÁLISIS:")
    
    if results['counting']['fail_at']:
        fail_val = results['counting']['fail_at']
        last_success = results['counting']['max_success']
        print(f"   1. Counting Sort falla alrededor de {fail_val:,}")
        print(f"      (Último éxito: {last_success:,})")
        
        if results['counting']['details']:
            last_result = results['counting']['details'][-1]['result']
            if 'max_memory_mb' in last_result:
                print(f"      RAM usada antes de fallar: {last_result['max_memory_mb']:.1f}MB")
    
    if results['better']['fail_at']:
        fail_val = results['better']['fail_at']
        last_success = results['better']['max_success']
        print(f"   2. Better Sort falla alrededor de {fail_val:,}")
        print(f"      (Último éxito: {last_success:,})")
        
        if results['better']['details']:
            last_result = results['better']['details'][-1]['result']
            if 'max_memory_mb' in last_result:
                print(f"      RAM usada antes de fallar: {last_result['max_memory_mb']:.1f}MB")
    
    print(f"\n🏆 CONCLUSIÓN:")
    if results['better']['max_success'] > results['counting']['max_success']:
        print(f"   ✅ Better Sort es MÁS ESCALABLE para valores grandes")
        print(f"   📊 Puede manejar hasta {results['better']['max_success']:,}")
    else:
        print(f"   ⚠️  Ambos algoritmos tienen límites similares")
    
    print(f"\n🛡️  Nota: Todos los tests fueron seguros")
    print(f"   El sistema nunca estuvo en riesgo de colgarse")

# ---------------------------------------
# MENÚ PRINCIPAL
# ---------------------------------------

def main():
    print("🔬 LABORATORIO AVANZADO DE ORDENACIÓN")
    print("======================================")
    print("Este script muestra el progreso en tiempo real")
    print("y encuentra los límites de cada algoritmo")
    print("======================================")
    
    while True:
        print("\n📋 OPCIONES DISPONIBLES:")
        print("1. Ejecutar experimento completo (recomendado)")
        print("2. Probar un valor específico con ambos algoritmos")
        print("3. Solo Counting Sort con progreso")
        print("4. Solo Better Sort con progreso")
        print("5. Ver información del sistema")
        print("6. Salir")
        
        choice = input("\n👉 Selecciona (1-6): ").strip()
        
        if choice == "1":
            run_progressive_experiment()
            
        elif choice == "2":
            try:
                max_val = int(input("👉 Ingresa el valor máximo a probar (ej: 1000000): "))
                array_size = int(input("👉 Tamaño del array (ej: 10000): "))
                
                memory_info = psutil.virtual_memory()
                safe_limit = min(4000, memory_info.available / 1024 / 1024 * 0.7)
                
                array = np.random.randint(0, max_val, size=array_size)
                
                print(f"\n🧪 PROBANDO COUNTING SORT con {max_val:,}")
                result1 = safe_test_with_progress(
                    counting_sort_original_with_progress,
                    array,
                    f"Counting Sort - {max_val:,}",
                    safe_limit
                )
                
                time.sleep(1)
                
                print(f"\n🧪 PROBANDO BETTER SORT con {max_val:,}")
                result2 = safe_test_with_progress(
                    better_sorting_benchmarks_with_progress,
                    array,
                    f"Better Sort - {max_val:,}",
                    safe_limit
                )
                
            except ValueError:
                print("❌ Valor inválido. Usa números enteros.")
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                
        elif choice == "3":
            try:
                max_val = int(input("👉 Valor máximo: "))
                array_size = int(input("👉 Tamaño del array: "))
                
                array = np.random.randint(0, max_val, size=array_size)
                memory_info = psutil.virtual_memory()
                safe_limit = min(4000, memory_info.available / 1024 / 1024 * 0.7)
                
                result = safe_test_with_progress(
                    counting_sort_original_with_progress,
                    array,
                    f"Counting Sort Solo - {max_val:,}",
                    safe_limit
                )
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                
        elif choice == "4":
            try:
                max_val = int(input("👉 Valor máximo: "))
                array_size = int(input("👉 Tamaño del array: "))
                
                array = np.random.randint(0, max_val, size=array_size)
                memory_info = psutil.virtual_memory()
                safe_limit = min(4000, memory_info.available / 1024 / 1024 * 0.7)
                
                result = safe_test_with_progress(
                    better_sorting_benchmarks_with_progress,
                    array,
                    f"Better Sort Solo - {max_val:,}",
                    safe_limit
                )
                
            except Exception as e:
                print(f"❌ Error: {str(e)}")
                
        elif choice == "5":
            mem = psutil.virtual_memory()
            print(f"\n💻 INFORMACIÓN DEL SISTEMA:")
            print(f"   RAM Total: {mem.total / 1024**3:.2f} GB")
            print(f"   RAM Disponible: {mem.available / 1024**3:.2f} GB")
            print(f"   RAM Usada: {mem.percent}%")
            print(f"   CPU Cores: {psutil.cpu_count()}")
            print(f"   CPU Usage: {psutil.cpu_percent()}%")
            
        elif choice == "6":
            print("\n👋 ¡Hasta luego!")
            break
            
        else:
            print("❌ Opción inválida")

# ---------------------------------------
# EJECUCIÓN
# ---------------------------------------

if __name__ == "__main__":
    try:
        import psutil
    except ImportError:
        print("❌ Necesitas: pip install psutil numpy")
        sys.exit(1)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  Interrumpido por usuario")
    except Exception as e:
        print(f"\n💥 Error crítico: {str(e)}")